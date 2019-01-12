class vec3():
	def __init__(self, x, y=None, z=None):
		if y is None and z is None:
			self.xyz = tuple(x)
		else:
			self.xyz = (x,y,z)
	def __add__(self, other):
		return vec3(x+y for (x,y) in zip(self.xyz, other.xyz))
	def __mul__(self, num):
		return vec3(num*x for x in self.xyz)
	def __div__(self, num):
		return vec3(x/num for x in self.xyz)
	__rmul__ = __mul__
	__floordiv__ = __div__
	__truediv__ = __div__
	def __repr__(self):
		return "<%0.2f, %0.2f, %0.2f>"%self.xyz