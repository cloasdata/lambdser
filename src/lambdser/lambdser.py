import marshal
import pickle
from types import LambdaType, FunctionType
from typing import List, Tuple

# todo register as pickler using copyreg?

T_ = Tuple[bytes, List[bytes]]


def install():
    # https://stackoverflow.com/q/2932742/18173142
    # todo not working yet
    import copyreg
    def _dumps(lambda_ex):
        pickle.dumps(dumps(lambda_ex))

    copyreg.pickle(LambdaType, _dumps)
    pickle._Pickler.dispatch[LambdaType] = _dumps


def cell(value):
    """
    Create a cell object
    https://stackoverflow.com/questions/37665862/how-to-create-new-closure-cell-objects
    :param value:
    :return:
    """
    return (lambda x: lambda: x)(value).__closure__[0]


def dumps(lambda_ex) -> T_:
    """
    Returns a serialize able tuple of a lambda expression including its closures
    """
    if isinstance(lambda_ex, LambdaType):
        if lambda_ex.__closure__:
            closures = [marshal.dumps(c.cell_contents) for c in lambda_ex.__closure__]
        else:
            closures = None
        code = marshal.dumps(lambda_ex.__code__)
        return code, closures
    else:
        raise TypeError(f"{LambdaType=} is not LambdaType")


def _loads(obj: T_, globals_):
    byte_code, byte_closures = obj
    code = marshal.loads(byte_code)
    if byte_closures:
        closures = tuple(cell(marshal.loads(c)) for c in byte_closures)
    else:
        closures = None
    return code, globals_, None, None, closures


def loads(serialized: T_, globals_=None) -> LambdaType:
    """
    Deserialize a lambda expression including its closures
    :param serialized: tuple
    :param globals_: provide on module level.
    :return: LambdaType

    """
    if not globals_:
        # this may provide wrong context
        globals_ = globals()
    args = _loads(serialized, globals_)
    return FunctionType(*args)


