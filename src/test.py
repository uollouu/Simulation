from entity import *
def f(*args):
    ar = []
    for i in args:
        ar.append(i)

    return ar

p = Rock()

print(f(copy(p),p,copy(p)))