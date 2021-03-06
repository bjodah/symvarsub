# -*- coding: utf-8 -*-

from __future__ import division, absolute_import


import sympy
from sympy import exp, Derivative
import numpy as np

from symvarsub import NumTransformer
from symvarsub.utilities import RealFunction


def test_NumTransformer(tempdir=None, logger=None):
    x, y = sympy.symbols('x y')
    t = NumTransformer([(x+1)**2, (x+1)**3-y], [x, y], tempdir=tempdir,
                       save_temp=True, logger=logger)
    x_, y_ = np.linspace(0, 10, 10), np.linspace(10, 20, 10)
    out = t(x_, y_)
    assert np.allclose(out, np.vstack(((x_+1)**2, (x_+1)**3-y_)).transpose())


def test_NumTransformer__complex_argument_names(tempdir=None, logger=None):
    # y'(t) = t**4; y(0)=1.0  ===> y = t**5/5 + 1.0
    # z(t) = log(y(t)) ===> y=exp(z(t)), dzdt = t**4*exp(-z(t))

    num_t = np.linspace(0.0, 3.0, 4)
    exact_y = num_t**5/5.0+1.0
    exact_dydt = num_t**4

    num_z = np.log(exact_y)
    num_dzdt = num_t**4*np.exp(-num_z)

    z = sympy.Function('z')
    t = sympy.Symbol('t')

    y_in_z = sympy.exp(z(t))
    dydt_in_z = y_in_z.diff(t)

    z_data = {t: num_t, z(t): num_z, z(t).diff(t): num_dzdt}

    exprs = [y_in_z, dydt_in_z]
    inp = [t, z(t), z(t).diff(t)]
    tfmr = NumTransformer(exprs, inp, tempdir=tempdir,
                          save_temp=True, logger=logger)
    result = tfmr(*[z_data[k] for k in inp])

    num_y = result[:, 0]
    assert np.allclose(num_y, exact_y)

    num_dydt = result[:, 1]
    assert np.allclose(num_dydt, exact_dydt)


def test_NumTransformer__complex_argument_names2(tempdir=None, logger=None):
    # y,t -> f,g
    # f = exp(y(t))
    # g = exp(y(t))*Derivative(y(t), t)

    n = 5
    num_y = np.linspace(5.0, 7.0, n)
    num_dydt = np.linspace(0.0, 3.0, n)

    exact_f = np.exp(num_y)
    exact_g = np.exp(num_y)*num_dydt

    out = ['f', 'g']
    exact = {'f': exact_f, 'g': exact_g}

    y = sympy.Function('y')
    t = sympy.Symbol('t')
    dydt = y(t).diff(t)

    exprs = [sympy.exp(y(t)), sympy.exp(y(t))*y(t).diff(t)]
    inp = [y(t), dydt]
    num_data = {y(t): num_y, dydt: num_dydt}
    tfmr = NumTransformer(exprs, inp, tempdir=tempdir,
                          save_temp=True, logger=logger)
    result = tfmr(*[num_data[k] for k in inp])

    for i, s in enumerate(out):
        assert np.allclose(result[:, i], exact[s])


def test_NumTransformer__write_code(tempdir=None, logger=None):
    t = sympy.Symbol('t', real=True)
    lny0, lny1, lny2, lny3, lny4 = [RealFunction(s)(t) for s
                                    in 'lny0 lny1 lny2 lny3 lny4'.split()]

    exprs = [
        exp(lny0), exp(lny0)*Derivative(lny0, t),
        exp(lny1), exp(lny1)*Derivative(lny1, t),
    ]
    args = [Derivative(lny1, t), lny1, Derivative(lny0, t), lny0]
    tfmr = NumTransformer(exprs, args, tempdir=tempdir, save_temp=True)
    # Compilation might fail: (that's what we are testing)
    tfmr(*([np.ones(3)]*len(args)))


if __name__ == '__main__':
    # When this test file is run from the command line
    # we print some extra info using a logger and save the generated
    # code in the output directories tmp${N}

    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    test_NumTransformer__complex_argument_names('./tmp1/', logger=logger)
    test_NumTransformer__complex_argument_names2('./tmp2/', logger=logger)
    test_NumTransformer('./tmp3/', logger=logger)
    test_NumTransformer__write_code(tempdir='./tmp4/', logger=logger)
