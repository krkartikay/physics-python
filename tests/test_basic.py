import physics

def test_resting():
	u = physics.Universe()
	p = physics.Particle((0,0,0), (0,0,0), 1)
	u.add(p)
	u.run(10)
	assert p.pos == (0,0,0)

def test_velocity():
	u = physics.Universe()
	p = physics.Particle((0,0,0), (1,2.5,-2), 1)
	u.add(p)
	u.run(10)
	assert p.pos == (10,25,-20)