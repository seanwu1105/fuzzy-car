def main():
    l = [1, 2, 3, 4]
    print(r(l))

def r(l):
    if len(l) == 2:
        return f(l[0], l[1])
    return f(l[0], r(l[1:]))

def f(a, b):
    return a * b

main()