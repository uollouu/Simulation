from entity import *
def f(*args):
    print(args)
    ar = []
    for i in args:
        ar.append(i)

    return ar

p = Rock()

print(f(copy(p),p,copy(p)))

l = [[2],[3]]
print(*l)