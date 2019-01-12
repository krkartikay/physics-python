"Single particle under influence of gravity"

import physics

u = physics.Universe(forces=[physics.GravityForce])

p = physics.Particle((0,0,0), (1,0,10), 1)

u.add(p)

while p.pos.xyz[2] >= 0:
	print("%0.3f"%u.time, p.pos)
	u.step()