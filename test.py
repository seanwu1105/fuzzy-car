class A(object):
    pass

class B(A):
    pass

a = A()
b = B()
print(type(b))
