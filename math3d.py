import math


class vec3():
    def __init__(self, x, y=None, z=None):
        if isinstance(x, vec3):
            self.xyz = x.xyz
            return
        if y is None and z is None:
            self.xyz = tuple(x)
        else:
            self.xyz = (x, y, z)

    def length(self):
        return math.sqrt(self * self)

    def unit(self):
        return self / self.length()

    def __add__(self, other):
        return vec3(x+y for (x, y) in zip(self.xyz, other.xyz))

    def __sub__(self, other):
        return self + (-1)*other

    def __neg__(self):
        return self * (-1)

    def __mul__(self, num):
        if type(num) == vec3:
            other = num
            return sum(x*y for (x, y) in zip(self.xyz, other.xyz))
        else:
            return vec3(num*x for x in self.xyz)

    def __div__(self, num):
        return vec3(x/num for x in self.xyz)
    __rmul__ = __mul__
    __floordiv__ = __div__
    __truediv__ = __div__

    def __repr__(self):
        return "vec3<%0.4f, %0.4f, %0.4f>" % self.xyz

    def __eq__(self, other):
        eps = 1e-4
        if isinstance(other, self.__class__):
            return all(abs(x - y) < eps for (x, y) in zip(self.xyz, other.xyz))
        elif isinstance(other, tuple):
            return all(abs(x - y) < eps for (x, y) in zip(self.xyz, other))
        else:
            return False

    def __nq__(self, other):
        return not self.__eq__(other)

    def data(self, dig=5):
        return [round(i, dig) for i in self.xyz]
