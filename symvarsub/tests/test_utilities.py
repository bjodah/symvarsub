import sympy

from utilities import MaybeRealFunction

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



if __name__ == '__main__':
    test_MaybeRealFunction()
