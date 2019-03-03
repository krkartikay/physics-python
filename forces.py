from math3d import vec3
from objects import *

class Force():
	def __init__(self):
		pass

	def getForce(self, p):
		pass


class GravityForce(Force):
	def __init__(self, g=vec3(0, 0, -1)):
		self.g = g

	def getForce(self, p):
		return p.mass * self.g


class SpringForce(Force):
	def getForce(self, p):
		F = vec3(0, 0, 0)
		for s in p.connections:
			if isinstance(s, Spring):
				F += s.getForce(p)
		return F

class DragForce(Force):
	def __init__(self, a=0.02):
		self.a = a

	def getForce(self, p: Particle):
		F = - self.a * p.vel * p.vel.length()
		return F
