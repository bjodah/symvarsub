# -*- coding: utf-8 -*-

from operator import attrgetter

import sympy

from symvarsub.utilities import (
    RealFunction, ImagFunction, reassign_const,
    # get_without_piecewise
)


def test_RealFunction_and_ImageFunction():
    x = sympy.Symbol('x')
    f = RealFunction('f')(x)
    assert f.is_real
    assert RealFunction('f')(x) == f

    ref_ccode = sympy.ccode(sympy.Function('f')(x))
    assert sympy.ccode(f) == ref_ccode

    y = sympy.Symbol('y', real=False)
    g = ImagFunction('g')(y)
    assert g.is_real is False
    assert f.is_real
    assert ImagFunction('g')(y) == g
    assert g != f
    assert RealFunction('f')(x) == f
    assert sympy.ccode(f) == sympy.ccode(sympy.Function('f')(x))


def test_reassign_const():
    x, C1, C2 = sympy.symbols('x C1 C2')
    new_expr, rea, not_rea = reassign_const(x*C1+C2, 'K', [x], 'C')
    assert not_rea == []
    K1, K2 = sympy.symbols('K1 K2')
    assert new_expr - x*K1 - K2 == 0
    assert sorted(rea, key=attrgetter('name')) == sorted(
        [K1, K2], key=attrgetter('name'))


# def test_get_without_piecewise():
#     x, k = sympy.symbols('x k')
#     f = sympy.Function('f')
#     dfdx_expr = x*sympy.exp(-k*x)
#     f_analytic = -(k*x+1)*sympy.exp(-k*x)/k**2
#     sol = sympy.dsolve(f(x).diff(x)-dfdx_expr, f(x))
#     without_piecewise, undefined = get_without_piecewise(sol.rhs)
#     # k != 0 (default)
#     assert (without_piecewise - f_analytic).simplify() == \
#         sympy.Symbol('C1')
#     # k == 0
#     assert undefined[0].rhs == 0
#     assert undefined[0].lhs.subs({k: 0}) == 0
