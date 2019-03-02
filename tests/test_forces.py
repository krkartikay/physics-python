import physics

def test_gravity():
	u = physics.Universe(timestep=0.0001)
	u.addForce(physics.GravityForce())
	p = physics.Particle((0, 0, 0), (0, 0, 0), 1)
	assert u.getForce(p) == (0, 0, -1)

def test_springForce():
	u = physics.Universe(timestep=0.0001)
	u.addForce(physics.SpringForce())
	p1 = physics.Particle((0, 0, 0), (0, 0, 0), 1)
	p2 = physics.Particle((1, 0, 0), (0, 0, 0), 1)
	s = physics.Spring(p1, p2, k=1.0)
	p2.setPos(2,0,0)
	assert u.getForce(p1) == (1, 0, 0)
	assert u.getForce(p2) == (-1, 0, 0)
