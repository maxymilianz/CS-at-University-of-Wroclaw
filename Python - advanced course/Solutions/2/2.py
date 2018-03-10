class Addable:
    def __add__(self, other):
        if not type(self) == type(other):       # I think it makes more sense than adding objects of different types
            print("Wrong type!")                # that both inherit from Addable (isinstance(other, Addable))
            return

        sum = Addable()

        for k, v in vars(self).items():
            setattr(sum, k, v)

        for k, v in vars(other).items():
            if k in vars(self):
                print(k, "defined in both objects, assigned value from first object!")
            else:
                setattr(sum, k, v)

        return sum

    def __radd__(self, other):      # makes it possible to add using function sum
        return self

class Engine(Addable):
    def __init__(self, **params):
        for param, val in params.items():
            setattr(self, param, val)

obj0 = Addable()
obj1 = Addable()

obj0.var0 = 1
obj0.var1 = 2
obj1.var1 = 3
obj1.var2 = 4

print(vars(obj0 + obj1))
print(vars(sum([obj0, obj1])))

e0 = Engine(power = 90, torque = 110)
e1 = Engine(power = 75, cylinders = 4)
print(vars(e0 + e1))