import sympy

from utilities import MaybeRealFunction

def test_MaybeRealFunction():
    x = sympy.Symbol('x')
    print sympy.ccode(sympy.Function('h')(x))
    print sympy.ccode(MaybeRealFunction('i', [x], real=True))

    f = MaybeRealFunction('f', [x], real=True)
    assert f.is_real

    # Sympy Caching most probably voids this test:
    assert MaybeRealFunction('f', [x], real=True) == f

    y = sympy.Symbol('y', real=False)
    g = MaybeRealFunction('g', [y], real=False)
    assert not g.is_real
    assert f.is_real
    assert MaybeRealFunction('g', [y], real=False) == g
    assert g != f
    assert MaybeRealFunction('f', [x], real=True) == f


if __name__ == '__main__':
    test_MaybeRealFunction()
