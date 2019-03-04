import math
from physics import *

u = Universe(timestep=0.0001)

u.addForce(SpringForce())
u.addForce(ImpulsiveForce())

num = 20

p_first = Particle((-num, 0, 0), (0, 0, 100), 1)

particles = [p_first]

for i in range(-num+1, num):
    particles += [Particle((i, 0, 0), (0, 0, 0), 1)]

p_last = FixedParticle((+num, 0, 0), (0, 0, -100), 1)

particles += [p_last]

for p in particles:
    u.add(p)

for i in range(len(particles) - 1):
    p1 = particles[i]
    p2 = particles[i+1]
    s = Spring(p1, p2, k=1000, l=0, damping=1)
    u.add(s)

# FOR TESTING
# u.addForce(GravityForce())
# p = Particle((0,0,0), (3,0,5), 1)
# u.add(p)

fl = open("data.txt", "w")

while u.time <= 10:
    u.infolog()
    d = str(u.data())
    d += '\n'
    fl.write(d)
    fl.flush()
    for i in range(50):
        u.step()
        if 10*u.time <= 2*math.pi:
            particles[0].pos = vec3(-num, 0, math.sin(10*u.time))
        else:
            particles[0].pos = vec3(-num, 0, 0)
