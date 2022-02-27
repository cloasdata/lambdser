import pickle
import lambdser


two = "2"
expression = lambda x: "number" + x + two

result1 = expression("4")
ser = lambdser.dumps(expression)
# now pickle can dump!
s = pickle.dumps(ser)
ser = pickle.loads(s)

# using on module level we need to invoke the global to give the lambda the correct context
expression = lambdser.loads(ser, globals_=globals())
result2 = expression("4")
assert result1 == result2