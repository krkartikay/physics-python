from math3d import vec3

class Particle():
	def __init__(self, pos, vel, mass):
		self.pos = vec3(pos)
		self.vel = vec3(vel)
		self.mass = mass
		self.universe = None
		self.connections = []
		self._new_pos = None
		self._new_vel = None

	def update(self):
		self.pos = self._new_pos
		self.vel = self._new_vel

	def setPos(self, *pos):
		self.pos = vec3(pos)

	def data(self):
		return {'pos': self.pos.data(), 'vel': self.vel.data(), 'mass': self.mass}

class FixedParticle(Particle):
	def update(self):
		self.pos = self.pos
		self.vel = vec3(0,0,0)
	
	def data(self):
		d = super().data()
		d['type'] = 'fixed'
		return d

class Spring():
	def __init__(self, p1: Particle, p2: Particle, k=1.0, l=None, damping=0.0):
		self.p1 = p1
		self.p2 = p2
		p1.connections += [self]
		p2.connections += [self]
		self.k = k
		self.c = damping
		if l is not None:
			self.l = l
		else:
			self.l = (p1.pos - p2.pos).length()

	def getForce(self, p):
		if not (p is self.p1 or p is self.p2):
			return vec3(0, 0, 0)
		elif p is self.p1:
			extension = (self.p2.pos - self.p1.pos).length() - self.l
			direction = (self.p2.pos - self.p1.pos).unit()
			springforce_magnitude = self.k*extension
			dampingforce_magnitude = self.c * ((self.p1.vel - self.p2.vel) * direction)
			magnitude = springforce_magnitude - dampingforce_magnitude
			force = magnitude * direction
			return force
		else:
			extension = (self.p1.pos - self.p2.pos).length() - self.l
			direction = (self.p1.pos - self.p2.pos).unit()
			springforce_magnitude = self.k*extension
			dampingforce_magnitude = self.c * ((self.p2.vel - self.p1.vel) * direction)
			magnitude = springforce_magnitude - dampingforce_magnitude
			force = magnitude * direction
			return force

	def data(self):
		return {'p1': self.p1.pos.data(), 'p2': self.p2.pos.data()}

class Impulse():
	def __init__(self, start=0, end=1, force=(0,0,0)):
		self.start = start
		self.end = end
		self.force = vec3(force)
	
	def getForce(self, p):
		if self.start <= p.universe.time <= self.end:
			return self.force
		else:
			return vec3(0,0,0)
