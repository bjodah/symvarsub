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
