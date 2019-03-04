from math3d import vec3
from objects import *


class Force():
	def __init__(self):
		pass

	def getForce(self, p):
		pass


class GravityForce(Force):
	def __init__(self, g=vec3(0, 0, -1)):
		self.g = vec3(g)

	def getForce(self, p):
		return p.mass * self.g


class SpringForce(Force):
	def getForce(self, p):
		F = vec3(0, 0, 0)
		for s in p.connections:
			if isinstance(s, Spring):
				F += s.getForce(p)
		return F


class QuadraticPotentialForce(Force):
	def __init__(self, k=1):
		self.k = k

	def getForce(self, p):
		return vec3(0,0, -self.k * p.pos.xyz[2])

class ImpulsiveForce(Force):
	def getForce(self, p):
		F = vec3(0, 0, 0)
		for x in p.connections:
			if isinstance(x, Impulse):
				F += x.getForce(p)
		return F


class DragForce(Force):
	def __init__(self, drag=0.02):
		self.a = drag

	def getForce(self, p: Particle):
		F = - self.a * p.vel * p.vel.length()
		return F
