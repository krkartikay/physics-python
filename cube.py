import math
from physics import *
from run_model import run

def main(u: Universe):
    u.addForce(SpringForce())
    u.addForce(GravityForce())
    u.addForce(GroundForce())
    u.addForce(WallForce(a=+30))
    u.addForce(WallForce(a=-30))

    center = vec3(-20, -15, 3)
    v_center = vec3(1, 0.4, 3.4)
    
    for i in [-1, 1]:
        for j in [-1, 1]:
            for k in [-1, 1]:
                pos = vec3(i, j, k)
                pos += center
                v_extra = vec3(0.3 if k==1 else -0.3, 0, 0)
                p = Particle(pos, v_center + v_extra, 1)
                u.add(p)
    
    for p1 in u.particles:
        for p2 in u.particles:
            if abs((p1.pos - p2.pos).length() - 2) < 0.01:
                s = Spring(p1, p2, k=1000, damping=10)
                u.add(s)
    
    p_center = Particle(center, v_center, 1)
    
    for p in u.particles:
        s = Spring(p, p_center, k=1000, damping=10)
        u.add(s)
    
    u.add(p_center)


run(main, accuracy=3, replay_speed=0.2)
