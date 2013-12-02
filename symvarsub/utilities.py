import sympy

def MaybeRealFunction(key, args, real=None):
    if real == None:
        return Function(key)(*args)
    try:
        ori_eval_is_real = sympy.Function._eval_is_real
    except AttributeError:
        ori_eval_is_real = None
    setattr(sympy.Function, '_eval_is_real', lambda self_: real)
    instance = sympy.Function(key)(*args)
    if ori_eval_is_real:
        setattr(sympy.Function, '_eval_is_real', ori_eval_is_real)
    else:
        delattr(sympy.Function, '_eval_is_real')
    return instance


def get_new_symbs(expr, known_symbs):
    new_symbs = set()
    for atom in expr.atoms():
        if not atom in known_symbs and not atom.is_Number:
            new_symbs.add(atom)
    return new_symbs


def reassign_const(expr, dest, known, source='C'):
    """
    e.g.
    >>> reassing_const(x*C1+C2, 'K', [x], 'C')
    x*K1+K2
    """
    def get_resymb(id_):
        tail = ''
        while sympy.Symbol(dest+id_+tail) in known:
            tail += 'A' # not pretty but should work..
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
