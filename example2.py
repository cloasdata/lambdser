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


if __name__ == "__main__":
    do_stuff()
