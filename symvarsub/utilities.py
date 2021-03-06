# -*- coding: utf-8 -*-

import sympy

from sympy import (
    Function, Dummy,
    # Symbol, Integer, Float,
)

from .core import replace_instances


def RealFunction(*args, **kwargs):
    instance = Function(*args, **kwargs)
    instance.is_real = True
    return instance


def ImagFunction(*args, **kwargs):
    instance = Function(*args, **kwargs)
    instance.is_real = False
    return instance


def get_new_symbs(expr, known_symbs):
    new_symbs = set()
    for atom in expr.atoms():
        if atom not in known_symbs and not atom.is_Number:
            new_symbs.add(atom)
    return new_symbs


def reassign_const(expr, dest, known, source='C'):
    """
    e.g.
    >>> x, C1, C2 = sympy.symbols('x C1 C2')
    >>> reassign_const(x*C1+C2, 'K', [x], 'C')[0]
    K1*x + K2
    """
    def get_resymb(id_):
        tail = ''
        while sympy.Symbol(dest+id_+tail) in known:
            tail += 'A'  # not pretty but should work..
        return sympy.Symbol(dest+id_+tail)

    new_symbs = get_new_symbs(expr, known)
    reassigned_symbs = []
    new_not_reassigned = []
    for symb in new_symbs:
        if source:
            # Only reassign matching source
            if symb.name.startswith(source):
                id_ = source.join(symb.name.split(source)[1:])
                resymb = get_resymb(id_)
                expr = expr.subs({symb: resymb})
                reassigned_symbs.append(resymb)
            else:
                # The new symb didn't match, store in
                # new_not_reassigned
                new_not_reassigned.append(symb)
        else:
            # All new symbs are to be renamed
            resymb = get_resymb(symb.name)
            expr.subs({symb: resymb})
            reassigned_symbs.append(resymb)
    return expr, reassigned_symbs, new_not_reassigned


def tokenize(expr):
    if isinstance(expr, sympy.Add):
        return '_add_'.join(map(tokenize, expr.args))
    elif isinstance(expr, sympy.Mul):
        return '_mul_'.join(map(tokenize, expr.args))
    elif isinstance(expr, sympy.Pow):
        return '_pow_'.join(map(tokenize, expr.args))
    elif isinstance(expr, sympy.Integer):
        if expr < 0:
            return 'minus_'+tokenize(-expr)
        return str(expr)
    elif isinstance(expr, sympy.Float):
        raise NotImplementedError
    else:
        return str(expr)


def dummify_Indexed(expr):
    indices_dummies = {}

    def get_indices_dummy(indices):
        if indices in indices_dummies:
            return indices_dummies[indices]
        dummy = sympy.Symbol('_'.join(map(tokenize, indices)))
        indices_dummies[indices] = dummy
        return dummy

    dummies = []

    def replacer(mtch):
        base, indices = mtch.base, mtch.indices
        index_dummy = get_indices_dummy(indices)
        dummy = sympy.Symbol(str(base)+'_'+str(index_dummy))
        dummies.append((dummy, (base, indices)))
        return dummy

    return replace_instances(expr, sympy.Indexed, replacer), dict(dummies)


def dummify_Indexed2(expr):
    indices_dummies = {}

    def get_indices_dummy(indices):
        if indices in indices_dummies:
            return indices_dummies[indices]
        dummy = Dummy()
        indices_dummies[indices] = dummy
        return dummy

    dummies = {}

    def replacer(mtch):
        dummy = Dummy()
        dummies[dummy] = mtch
        return dummy

    return replace_instances(expr, sympy.Indexed, replacer), dummies


# def get_without_piecewise(expr):
#     """
#     Example:
#     >>> x, k = sympy.symbols('x k')
#     >>> f = sympy.Function('f')
#     >>> dfdx_expr = x*sympy.exp(-k*x)
#     >>> sol = sympy.dsolve(f(x).diff(x) - dfdx_expr, f(x))
#     >>> print(sol)
#     f(x) == C1 + Piecewise((x**2/2, k**3 == 0), \
# ((-k**2*x - k)*exp(-k*x)/k**3, True))
#     >>> wo, undef = get_without_piecewise(sol.rhs)
#     >>> print(wo)
#     C1 + (-k**2*x - k)*exp(-k*x)/k**3
#     """
#     undefined = []

#     def replacer(mtch):
#         result = None
#         for internal_expr, cond in mtch.args:
#             if cond is True:
#                 result = internal_expr
#             else:
#                 undefined.append(cond)
#         return result
#     return replace_instances(expr, sympy.Piecewise, replacer), undefined
