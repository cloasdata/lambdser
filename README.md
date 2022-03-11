# lambdser

A lambda expression serializer for python. Can be used to make pickle eat lambdas with closures.

A typical use case is serializing lambdas for multiprocessing. Using lambdser in front, let multiprocessing eat
the lambda expression.

## Install

    pip install lambdser

or install it from github
    
    pip install git+https://github.com/cloasdata/lambdser.git

or just clone it

## todo

I did not find a way to register lambdser es pickler in the pickle module. It would be really useful
if somebody can help me. However, one can use the LambdserPickler class 
to overwrite the default behaviour of pickle.Pickler (?) or use LamdserPickler as the one pickler.

I also did not test for particular edge cases. But feel free to contribute such tests.


## usage

### Example 1: module namespace

using it in module namespace.

``` python
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
```

### Example 2: Using closure

Make a proxy of what you want to spawn in a separate process.

``` python
    import lambdser
    import multiprocessing as mp
    
    
    def make_proxy(para, *funcs):
        # make proxy for the mp
        ser_list = []
        for f in funcs:
            ser_list.append(lambdser.dumps(f))
        return para, ser_list
    
    
    def processor(*ser):
        # unzip the proxy and to the work
        para, funcs = ser
        funcs = [lambdser.loads(ser) for ser in funcs]
        res = None
        for f in funcs:
            res = f(para)
        print(res)
        return res
    
    
    def do_stuff():
        two = "2"
        ser = make_proxy("4", lambda x: x + two)
        mp.Process(target=processor, args=ser).start()

    do_stuff()
```

## performance

it is around 100 times faster than dill. This was one reason to develop this package. 
    
    py .\test\profiling.py

    Results dumps
    lambdser: 0.012459
    dill:     1.485589
    times:    119.236291
