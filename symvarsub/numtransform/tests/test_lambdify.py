# -*- coding: utf-8 -*-

from __future__ import division

from sympy import sin, cos, sqrt, symbols, pi

from symvarsub import lambdify

x, y = symbols('x, y')


# Testing a relaxed sub set of sympy's test_lambdify

def test_single_arg():
    f = lambdify(x, 2*x)
    assert f(1) == 2


def test_list_args():
    f = lambdify([x, y], x + y)
    assert f(1, 2) == 3


def test_exponentiation():
    f = lambdify(x, x**2)
    assert f(-1) == 1
    assert f(0) == 0
    assert f(1) == 1
    assert f(-2) == 4
    assert f(2) == 4
    assert f(2.5) == 6.25


def test_sqrt():
    f = lambdify(x, sqrt(x))
    assert f(0) == 0.0
    assert f(1) == 1.0
    assert f(4) == 2.0
    assert abs(f(2) - 1.414) < 0.001
    assert f(6.25) == 2.5


def test_trig():
    f = lambdify([x], [cos(x), sin(x)])
    d = f(pi)
    prec = 1e-11
    print(d)
    assert abs(d[0] + 1) < prec
    assert abs(d[1]) < prec
    d = f(3.14159)
    prec = 1e-5
    assert abs(d[0] + 1) < prec
    assert abs(d[1]) < prec
