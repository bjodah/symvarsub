# -*- coding: utf-8 -*-

import sympy

from symvarsub.utilities import MaybeRealFunction, reassign_const, get_without_piecewise

def test_MaybeRealFunction():
    x = sympy.Symbol('x')
    f = MaybeRealFunction('f', [x], real=True)
    assert f.is_real
    assert MaybeRealFunction('f', [x], real=True) == f

    ref_ccode = sympy.ccode(sympy.Function('f')(x))
    assert sympy.ccode(f) == ref_ccode

    y = sympy.Symbol('y', real=False)
    g = MaybeRealFunction('g', [y], real=False)
    assert not g.is_real
    assert f.is_real
    assert MaybeRealFunction('g', [y], real=False) == g
    assert g != f
    assert MaybeRealFunction('f', [x], real=True) == f
    assert sympy.ccode(f) == sympy.ccode(sympy.Function('f')(x))

def test_reassign_const():
    x, C1, C2 = sympy.symbols('x C1 C2')
    new_expr, rea, not_rea = reassign_const(x*C1+C2, 'K', [x], 'C')
    assert not_rea == []
    K1, K2 = sympy.symbols('K1 K2')
    assert new_expr - x*K1 - K2 == 0
    assert rea == [K1, K2]

def test_get_without_piecewise():
    x, k = sympy.symbols('x k')
    f = sympy.Function('f')
    dfdx_expr = x*sympy.exp(-k*x)
    f_analytic = -(k*x+1)*sympy.exp(-k*x)/k**2
    sol = sympy.dsolve(f(x).diff(x)-dfdx_expr,f(x))
    without_piecewise, undefined = get_without_piecewise(sol.rhs)
    # k != 0 (default)
    assert (without_piecewise - f_analytic).simplify() == \
        sympy.Symbol('C1')
    # k == 0
    assert undefined[0].rhs == 0
    assert undefined[0].lhs.subs({k:0}) == 0
