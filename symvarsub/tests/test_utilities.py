import sympy

from symvarsub.utilities import MaybeRealFunction, reassign_const

def test_MaybeRealFunction():
    x = sympy.Symbol('x')
    ref_ccode = sympy.ccode(sympy.Function('f')(x))
    f = MaybeRealFunction('f', [x], real=True)
    assert f.is_real
    assert MaybeRealFunction('f', [x], real=True) == f
    sympy.ccode(f) == ref_ccode

    y = sympy.Symbol('y', real=False)
    g = MaybeRealFunction('g', [y], real=False)
    assert not g.is_real
    assert f.is_real
    assert MaybeRealFunction('g', [y], real=False) == g
    assert g != f
    assert MaybeRealFunction('f', [x], real=True) == f
    sympy.ccode(f) == sympy.ccode(sympy.Function('f')(x))

def test_reassign_const():
    x, C1, C2 = sympy.symbols('x C1 C2')
    new_expr, rea, not_rea = reassign_const(x*C1+C2, 'K', [x], 'C')
    assert not_rea == set([])
    K1, K2 = sympy.symbols('K1 K2')
    assert new_expr - x*K1 - K2 == 0
    assert rea == set([K1, K2])


if __name__ == '__main__':
    test_MaybeRealFunction()
    test_reassign_const()
