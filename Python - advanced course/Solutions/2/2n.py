from abc import ABC, abstractmethod
from itertools import product

class Formula(ABC):
    @abstractmethod
    def compute(self, vars):
        pass

    @abstractmethod
    def find_vars(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

class Not(Formula):
    def __init__(self, f):
        self.f = f

    def compute(self, vars):
        return not self.f.compute(vars)

    def find_vars(self):
        return self.f.find_vars()

    def __str__(self):
        return 'not (' + str(self.f) + ')'

class Or(Formula):
    def __init__(self, fl, fr):
        self.fl = fl
        self.fr = fr

    def compute(self, vars):
        return self.fl.compute(vars) or self.fr.compute(vars)

    def find_vars(self):
        return self.fl.find_vars() | self.fr.find_vars()

    def __str__(self):
        return '(' + str(self.fl) + ') or (' + str(self.fr) + ')'

class And(Formula):
    def __init__(self, fl, fr):
        self.fl = fl
        self.fr = fr

    def compute(self, vars):
        return self.fl.compute(vars) and self.fr.compute(vars)

    def find_vars(self):
        return self.fl.find_vars() | self.fr.find_vars()

    def __str__(self):
        return '(' + str(self.fl) + ') and (' + str(self.fr) + ')'

class Impl(Formula):
    def __init__(self, fl, fr):
        self.fl = fl
        self.fr = fr

    def compute(self, vars):
        return not (self.fl.compute(vars) and not self.fr.compute(vars))

    def find_vars(self):
        return self.fl.find_vars() | self.fr.find_vars()

    def __str__(self):
        return '(' + str(self.fl) + ') => (' + str(self.fr) + ')'

class Eq(Formula):
    def __init__(self, fl, fr):
        self.fl = fl
        self.fr = fr

    def compute(self, vars):
        return self.fl.compute(vars) == self.fr.compute(vars)

    def find_vars(self):
        return self.fl.find_vars() | (self.fr.find_vars())

    def __str__(self):
        return '(' + str(self.fl) + ') <=> (' + str(self.fr) + ')'

class Const(Formula):
    def __init__(self, b):
        self.b = b

    def compute(self, vars):
        return self.b

    def find_vars(self):
        return set()

    def __str__(self):
        return str(self.b)

class Var(Formula):
    def __init__(self, name):
        self.name = name

    def compute(self, vars):
        return vars[self.name]

    def find_vars(self):
        return {self.name}

    def __str__(self):
        return self.name

def print_formula(f, vars):
    print(f, '=', f.compute(vars))

def tautology(f):
    found_vars = f.find_vars()

    for vars in [{var: val for (var, val) in zip(found_vars, vals)} for vals in product([False, True], repeat = len(found_vars))]:
        if not f.compute(vars):
            return False

    return True

var0 = Var("var0")
var1 = Var("var1")

true = Const(True)
false = Const(False)

formula0 = Not(Or(And(var0, true), Impl(Eq(var1, false), var0)))
print_formula(formula0, {"var0": True, "var1": False})
print_formula(formula0, {"var0": False, "var1": True})

print(tautology(formula0))

de_morgan_1 = Eq(Not(And(Var('p'), Var('q'))), Or(Not(Var('p')), Not(Var('q'))))
de_morgan_2 = Eq(Not(Or(Var('p'), Var('q'))), And(Not(Var('p')), Not(Var('q'))))
clavius = Impl(Impl(Not(Var('p')), Var('p')), Var('p'))

for formula in [de_morgan_1, de_morgan_2, clavius]:
    print(tautology(formula))