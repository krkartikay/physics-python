import math
from physics import *

u = Universe(timestep=0.0005)

u.addForce(SpringForce())
u.addForce(GravityForce())
u.addForce(GroundForce())
u.addForce(WallForce(a=+30))
u.addForce(WallForce(a=-30))

particles = []

N = 6

for i in range(N):
    a = 2*math.pi * i/N
    x, y = math.cos(a), math.sin(a)
    vx, vz, vy = math.sin(a), -math.cos(a), 0 # math.sin(a)
    x += -25
    y += +6
    vx += 1.4
    vz += 2.7
    p = Particle((x, 0, y), (vx, vy, vz), 1)
    particles += [p]
    u.add(p)

px = Particle((-25, 0, 6), (1.4, 0, 2.7), 1)
u.add(px)

for i in range(len(particles)):
    p1, p2 = particles[i], particles[i-1]
    s = Spring(p1, p2, k=1000, damping=10)
    u.add(s)
    p1, p2 = particles[i], px
    s = Spring(p1, p2, k=1000, damping=10)
    u.add(s)

fl = open("data.txt", "w")

while u.time <= 100:
    u.infolog()
    d = str(u.data())
    d += '\n'
    fl.write(d)
    fl.flush()
    for i in range(50):
        u.step()
