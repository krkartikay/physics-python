import math
from physics import *
from run_model import run

def main(u: Universe):
    u.addForce(SpringForce())
    u.addForce(GravityForce())
    u.addForce(GroundForce())
    u.addForce(WallForce(a=+30))
    u.addForce(WallForce(a=-30))

    p = Particle((0,0,0), (2,0,2), 1)
    u.add(p)

run(main, 1, 5)