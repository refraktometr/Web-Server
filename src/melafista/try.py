class YesInit:
    def __init__(self,one,two):
        self.fname = one
        self.sname = two

obj1 = YesInit("Peter","Ok")

print (obj1.fname, obj1.sname)


class NoInit:
    def names(self,one,two):
        self.fname = one
        self.sname = two

obj1 = NoInit()
obj1.names("Peter","Ok")

print (obj1.fname, obj1.sname)