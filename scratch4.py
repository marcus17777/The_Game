__author__ = 'Markus Peterson'


class asi:
    def __init__(self, value):
        self.value = value

    def __getitem__(self, item):
        print(item)
        return self.value[item[0]], self.value[item[1]]


a = asi([0, 1, 2, 3])

print(a[0, 2])
