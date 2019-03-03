from math3d import vec3
from objects import *
from forces import *

class Universe():
	def __init__(self, timestep=0.001):
		self.forces = []
		self.particles = []
		self.springs = []
		self.time = 0
		self.timestep = timestep
	
	def addForce(self, f):
		self.forces += [f]

	def add(self, x):
		if isinstance(x, Particle):
			self.particles += [x]
			x.universe = self
		elif isinstance(x, Spring):
			self.springs += [x]
			x.universe = self

	def getForce(self, p):
		F = vec3(0,0,0)
		for force in self.forces:
			F += force.getForce(p)
		return F

	def step(self):
		"Forward Euler Step Forward"
		# for each particle calculate total force acting on it
		dt = self.timestep
		for p in self.particles:
			F = self.getForce(p)
			acc = F/p.mass
			p._new_pos = p.pos + dt * p.vel
			p._new_vel = p.vel + dt * acc
		# for double buffering
		for p in self.particles:
			p.update()
		self.time += dt

	def run(self, time = 1):
		while abs(self.time - time) > 1e-7:
			self.step()
		
	def data(self):
		pdata = [p.data() for p in self.particles]
		sdata = [s.data() for s in self.springs]
		return {'particles': pdata, 'springs': sdata}
