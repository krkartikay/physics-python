import physics

def test_particle_data():
	u = physics.Universe()
	p = physics.Particle((0,0,0),(1,1,1),1)
	u.add(p)
	p = physics.Particle((1,2,3),(2,-1,2),4)
	u.add(p)
	expected = {'p1': {'pos': [0, 0, 0], 'vel': [1, 1, 1], 'mass': 1}, 'p2': {'pos': [1, 2, 3], 'vel': [2, -1, 2], 'mass': 4}}
	assert u.data() == expected
