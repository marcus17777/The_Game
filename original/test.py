import test2

__author__ = 'Markus Peterson'


class Test(test2.Test2):
    def __init__(self, _var):
        self.var = _var


g = Test(test2.Test2.muutuja)

print(g.var, test2.Test2.muutuja)
g.var = 9
print(g.var, test2.Test2.muutuja)
