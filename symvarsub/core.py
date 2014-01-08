# -*- coding: utf-8 -*-

def replace_instances(expr, MatchingClass, replacer):
    """
    Example:
    >>> x = Symbol('x')
    >>> expr = x + Piecewise((x**2, x<2), (x**3, True))
    >>> new_expr = replace_instances(epxr,
    ...     lambda x: isinstance(x, Piecewise),
    ...     lambda p: filter(itemgetter(1), p.args)[0].args[0])
    >>> print(new_expr)
    x + x**3
    """
    if isinstance(expr, MatchingClass):
        return replacer(expr)
    else:
        new_args = []
        for arg in expr.args:
            if arg.has(MatchingClass):
                new_args.append(replace_instances(
                    arg, MatchingClass, replacer))
            else:
                new_args.append(arg)
        return expr.fromiter(new_args)
