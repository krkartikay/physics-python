import physics

def test_particle_data():
    u = physics.Universe()
    p = physics.Particle((0, 0, 0), (1, 1, 1), 1)
    u.add(p)
    p = physics.Particle((1, 2, 3), (2, -1, 2), 4)
    u.add(p)
    expected = [{'mass': 1, 'pos': [0, 0, 0], 'vel': [1, 1, 1]},
                              {'mass': 4, 'pos': [1, 2, 3], 'vel': [2, -1, 2]}]
    d = u.data()
    assert d['particles'] == expected
