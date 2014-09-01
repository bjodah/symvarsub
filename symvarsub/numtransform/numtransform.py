# -*- coding: utf-8 -*-

"""
Lightning fast binary callbacks using F90 for array expressions
"""

import os
from functools import partial
from collections import defaultdict

import sympy
from sympy.core.compatibility import iterable
import numpy as np
from pycompilation import import_module_from_file, FileNotFoundError
from pycompilation.compilation import FortranCompilerRunner
from pycompilation.util import HasMetaData
from pycodeexport.codeexport import F90_Code, DummyGroup, ArrayifyGroup


def lambdify(args, expr, **kwargs):
    """
    Mimics from sympy.utilities.lambdify.lambdify
    but allows to use numpy arrays
    """
    if isinstance(args, sympy.Symbol):
        args = [args]
    if not isinstance(expr, list) and not isinstance(expr, tuple):
        expr = [expr]
    return NumTransformer(expr, args, **kwargs)


class NumTransformer(F90_Code, HasMetaData):
    """
    The the Transformer instance can export expressions
    (given in `exprs`) to C/Fortran and compile callbacks
    which takes input arrays/scalars (given in `inp`).
    The callback returns a two dimesional array with
    shape: (len(exprs), len(inp))
    """

    templates = ['transform_template.f90']

    build_files = [
        'prebuilt/transform_wrapper.o',
        'prebuilt/'+FortranCompilerRunner.metadata_filename, # <- Ensure we compile with same compiler
    ]

    source_files = ['transform.f90']

    obj_files = [
        'transform.o',
        'transform_wrapper.o',
    ]

    so_file = 'transform_wrapper.so'

    compile_kwargs = {'options': ['pic', 'warn', 'fast']}

    def __init__(self, exprs, inp, **kwargs):
        self._exprs = exprs
        self._inp = inp

        self._cached_files = self._cached_files or []
        self.basedir = os.path.dirname(__file__)

        self._robust_exprs, self._robust_inp_symbs, self._robust_inp_dummies = \
            self.robustify(self._exprs, self._inp)

        super(NumTransformer, self).__init__(**kwargs)
        # Make sure our self._tempdir has not been used
        # previously by another NumTransformer instance
        # (if it has import of the .so file will fail)
        # due to caching of python (if imported previously
        # in this running Python interpreter session)

        try:
            hash_ = self.get_from_metadata_file(self._tempdir, 'hash')
            if hash_ == hash(self):
                try:
                    self._binary_mod = import_module_from_file(self.binary_path)
                except ImportError:
                    raise ImportError('Failed to import module, try to remove "{}" in "{}"'.format(
                        self.metadata_filename, self._tempdir))
            else:
                raise ValueError("Hash mismatch (current, old): {}, {}".format(
                    hash(self), hash_))
        except FileNotFoundError:
            self._binary_mod = self.compile_and_import_binary()
            self.save_to_metadata_file(self._tempdir, 'hash', hash(self))


    def __hash__(self):
        """
        Due to shortcomings of pythons import mechanisms (or *nix OSes?)
        it is not (easily?) possible to reimport a .so file from the _same_
        path if it has been updated. The work-around chosen here
        is to generate a unique `so_file` name for the instance.

        Note that we are not guaranteeing absence of hash collisions...
        """
        return hash(tuple(self._exprs)+tuple(self._inp))


    def robustify(self, exprs, inp):
        dummies = []
        def make_dummy(key, not_in_any):
            if isinstance(key, sympy.Function):
                candidate = sympy.Symbol(key.func.__name__, real=key.is_real)
            elif isinstance(key, sympy.Derivative):
                candidate = sympy.Symbol('d'+key.args[0].func.__name__+\
                                         ''.join('d'+x.name for x in key.args[1:]))
            elif isinstance(key, sympy.Symbol):
                candidate = key
            elif isinstance(key, str):
                candidate = sympy.Symbol(key)
            else:
                raise NotImplementedError
            # Now lets make sure the dummie symbol is unique
            if candidate not in dummies and not any(
                    [not_in.has(candidate) for not_in in not_in_any]):
                dummies.append(candidate)
                return candidate
            else:
                return make_dummy(candidate.name+'p', not_in)

        # First let's determine the used keys
        used_keys = []
        used_keys_dummies = []
        derivs = defaultdict(dict)
        any_expr_has = lambda x: any([expr.has(x) for expr in exprs])
        for key in filter(any_expr_has, inp):
            used_keys.append(key)
            if isinstance(key, sympy.Symbol):
                used_keys_dummies.append(key)
            else:
                new_dummy = make_dummy(key, not_in_any=exprs)
                used_keys_dummies.append(new_dummy)
                # Determine order of derivative
                if isinstance(key, sympy.Derivative):
                    derivorder = len(key.args)-1
                    derivs[derivorder][key] = new_dummy
                elif isinstance(key, sympy.Function):
                    derivorder = 0
                    derivs[derivorder][key] = new_dummy
                elif isinstance(key, sympy.Symbol):
                    pass
                else:
                    raise NotImplementedError

        for n in sorted(derivs.keys())[::-1]:
            # Substitutions of symbolified derivatives
            # need to be made for the highest degrees of
            # derivatives first
            for deriv, symb in derivs[n].items():
                exprs = [expr.subs({deriv: symb}) for expr in exprs]

        # Ok, so all Derivative(...) instances in exprs should have
        # been dummyfied - iff user provided all corresponding Derivative(...)
        # as inputs, let's check that now and stop them if they missed any:
        if any_expr_has(sympy.Derivative): raise ValueError(
                'Did you forget to provide all derivatives as input?')

        # Now we are almost there..
        # But e.g. z(t) has included t into used_keys
        # we need to double check that t is truly used
        # now that z(t) has been turned into z
        truly_used_keys, truly_used_keys_dummies = [], []
        for k, ks in zip(used_keys, used_keys_dummies):
            if any_expr_has(ks):
                truly_used_keys.append(k)
                truly_used_keys_dummies.append(ks)

        return exprs, truly_used_keys, truly_used_keys_dummies


    def __call__(self, *args):
        """
        Give arrays in as arguments in same order as `inp` at init.
        """
        if self._binary_mod.__file__ != self.binary_path:
            # Avoid singleton behaviour. (Python changes binary path
            # inplace without changing id of Python object)
            self._binary_mod = import_module_from_file(self.binary_path)
        if self._binary_mod.__file__ != self.binary_path:
            raise RuntimeError
        dummies = dict(zip(self._robust_inp_symbs, self._robust_inp_dummies))
        idxs = [self._inp.index(symb) for symb in self._robust_inp_symbs]
        # make sure args[i] 1 dimensional: .reshape(len(args[i]))
        inp = np.vstack([np.array(args[i], dtype=np.float64) for i in idxs]).transpose()
        ret = self._binary_mod.transform(inp, len(self._exprs))
        if len(self._exprs) == 1 and len(args) == 1:
            if isinstance(args[0], float): return ret[0][0]
        elif all([not iterable(arg) for arg in args]):
            return ret[0]
        return ret


    def variables(self):
        dummy_groups = (
            DummyGroup('argdummies', self._robust_inp_dummies),
            )
        arrayify_groups = (
            ArrayifyGroup('argdummies', 'input', 1, 1),
        )

        cse_defs_code, exprs_in_cse_code = self.get_cse_code(
            self._robust_exprs, 'cse', dummy_groups, arrayify_groups)

        return {'CSES': cse_defs_code,
                'EXPRS_IN_CSE': exprs_in_cse_code,
                'N_EXPRS': len(self._exprs),
                'N_ARGS': len(self._robust_inp_dummies)}
