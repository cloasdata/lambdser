import pytest
import pickle
import dill

import src.lambdser as lambdser


@pytest.fixture()
def lambda_closure():
    fine = "fine"
    stop = "."
    return lambda x: x + "works " + fine + stop


@pytest.fixture()
def lambda_no_closure():
    return lambda x: x + "works fine."


@pytest.mark.parametrize(
    "lambdas", ["lambda_closure", "lambda_no_closure"]
)
class TestLambler:
    def test_dumps(self, lambdas, request):
        lambda_ = request.getfixturevalue(lambdas)
        bytes_ = lambdser.dumps(lambda_)
        pickled = pickle.dumps(bytes_)
        assert pickled

    def test_loads(self, lambdas, request):
        lambda_ = request.getfixturevalue(lambdas)
        bytes_ = lambdser.dumps(lambda_)
        func = lambdser.loads(bytes_)
        assert func("this ") == "this works fine."

    def test_dump_non_lambda(self, lambdas):
        with pytest.raises(TypeError) as e:
            ser = lambdser.dumps("sd")
        assert e

    def test_lambdser_dumps(self, lambdas, request, benchmark):
        lambda_ = request.getfixturevalue(lambdas)
        benchmark(lambda: pickle.dumps(lambdser.dumps(lambda_)))

    def test_dill_dumps(self, lambdas, request, benchmark):
        lambda_ = request.getfixturevalue(lambdas)

        benchmark(lambda: dill.dumps(lambda_))

    def test_lambdser_loads(self, lambdas, request, benchmark):
        lambda_ = request.getfixturevalue(lambdas)
        bytes_ = lambdser.dumps(lambda_)
        benchmark(lambda: lambdser.loads(bytes_))

    def test_dill_loads(self, lambdas, request, benchmark):
        lambda_ = request.getfixturevalue(lambdas)
        bytes_ = dill.dumps(lambda_)
        benchmark(lambda: dill.loads(bytes_))