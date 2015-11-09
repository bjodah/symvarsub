# -*- coding: utf-8 -*-


def replace_instances(expr, MatchingClass, replacer):
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
