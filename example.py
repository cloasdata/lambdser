import pickle
import lambdser


two = "2"
expression = lambda x: "number" + x + two

result1 = expression("4")
ser = lambdser.dumps(expression)
# now pickle can dump!
s = pickle.dumps(ser)
ser = pickle.loads(s)

expression = lambdser.loads(ser)
result2 = expression("4")
assert result1 == result2