from math3d import vec3

# all units are in SI

class Universe():
	def __init__(self, forces, timestep=0.001):
		self.forces = forces
		self.objects = []
		self.time = 0
		self.timestep = timestep

	def add(self, p):
		self.objects += [p]
		p.universe = self

	def getForce(self, p):
		F = vec3(0,0,0)
		for force in self.forces:
			F += force(p)
		return F

	def step(self):
		"Forward Euler Step Forward"
		# for each particle calculate total force acting on it
		dt = self.timestep
		particles = filter(lambda p: isinstance(p, Particle), self.objects)
		for p in particles:
			F = self.getForce(p)
			acc = F/p.mass
			p._new_pos = p.pos + dt * p.vel
			p._new_vel = p.vel + dt * acc
		# for double buffering
		particles = filter(lambda p: isinstance(p, Particle), self.objects)
		for p in particles:
			p.update()
		self.time += dt

	def run(self, time = 1):
		while abs(self.time - time) > 1e-7:
			self.step()

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

class Spring():
	def __init__(self, p1, p2, k = 1.0, l = None):
		self.p1 = p1
		self.p2 = p2
		self.k = k
		if l is not None:
			self.l = l
		else:
			self.l = (p1-p2).length()

def GravityForce(p):
	g = vec3(0,0,-9.8)
	return p.mass * g