import pickle

class DumClass:
    def __init__(self):
        self.paramA = 1
        self.paramB = 'B'

    def foo(self):
        print(self.paramA)


# t = DumClass()
# with open('dum','wb') as fn:
#     pickle.dump(t, fn)

with open('dum', 'rb') as fn:
    t = pickle.load(fn)

t.foo()