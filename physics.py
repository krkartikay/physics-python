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
		particles = filter(lambda p: type(p)==Particle, self.objects)
		timestep = self.timestep
		for p in particles:
			F = self.getForce(p)
			acc = F/p.mass
			p.pos += timestep * p.vel
			p.vel += timestep * F
		self.time += timestep

class Particle():
	def __init__(self, pos, vel, mass):
		self.pos = vec3(pos)
		self.vel = vec3(vel)
		self.mass = mass
		self.universe = None

def GravityForce(p):
	g = vec3(0,0,-9.8)
	return p.mass * g