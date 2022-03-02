import copy
import marshal
import pickle
from types import LambdaType, FunctionType
from typing import Callable
import inspect


class LambdserPickler(pickle.Pickler):
    def reducer_override(self, obj):
        if is_lambda(obj):
            arg = dumps(obj)
            return loads, (arg,), None, None, None, None
        else:
            return NotImplemented


# def install():
#     # https://stackoverflow.com/q/2932742/18173142
#     # todo not working yet
#     # todo the function provided to pickle must return the reduce signature.
#     # https://docs.python.org/3/library/pickle.html#object.__reduce__
#     import copyreg

#     copyreg.pickle(LambdaType, reduce)


def cell(value):
    """
    Create a cell object
    https://stackoverflow.com/questions/37665862/how-to-create-new-closure-cell-objects
    :param value:
    :return:
    """
    return (lambda x: lambda: x)(value).__closure__[0]


def dumps(lambda_ex, *, transfer_global=False) -> bytes:
    """
    Dumps the lambda expression to a byte string.
    Can be used than to pickle further.
    Uses marshall under the hood.
    :param lambda_ex: Lambda expression
    :param transfer_global: set true the global context of the lambda will be copied. Attention: can be harmfull
    :return: bytes

    """
    if is_lambda(lambda_ex):
        return _dumps(lambda_ex, transfer_global)
    else:
        raise TypeError(f"{LambdaType=} is not LambdaType. Lambdser only supports lambda.")


def _dumps(lambda_ex, transfer_global=False):
    if transfer_global:
        func_globals = inspect.stack()[1].frame.f_globals
        names = get_names(lambda_ex)
        globals_ = {name: copy.copy(func_globals[name]) for name in names}
    else:
        globals_ = None

    if has_closures(lambda_ex):
        closures = [c.cell_contents for c in lambda_ex.__closure__]
    else:
        closures = None
    # code = marshal.dumps(lambda_ex.__code__)
    code = lambda_ex.__code__
    return marshal.dumps((code, closures, globals_))


def loads(serialized: bytes) -> LambdaType:
    """
    Deserialize a lambda expression including its closures
    :param serialized: tuple
    :return: LambdaType

    """
    # get context of callee
    _globals = inspect.stack()[1].frame.f_globals
    args = _loads(serialized, _globals)
    return FunctionType(*args)


def _loads(obj: bytes, globals_):
    code, closures, func_globals = marshal.loads(obj)
    if closures:
        closures = tuple(cell(c) for c in closures)
    if func_globals:
        globals_.pop(func_globals)
    return code, globals_, None, None, closures


def is_lambda(obj: Callable) -> bool:
    if isinstance(obj, LambdaType):
        return obj.__code__.co_name == "<lambda>"
    else:
        return False


def has_closures(obj) -> bool:
    return obj.__closure__


def get_names(lambda_):
    return lambda_.__code__.co_names

