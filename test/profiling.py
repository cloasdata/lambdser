import timeit
import lambdser
import dill

NUMBER = 10_000

two = "2"

lambda_exp = lambda x: x+ "4" + two

res_lambdser = timeit.timeit("lambdser.dumps(lambda_exp)", globals=globals(), number=NUMBER)
res_dill =  timeit.timeit("dill.dumps(lambda_exp)", globals=globals(), number=NUMBER)

results = f"Results dumps\n" \
          f"lambdser: {res_lambdser:2f}\n" \
          f"dill:     {res_dill:2f}\n" \
          f"times:    {res_dill/res_lambdser:2f}"


print(results)