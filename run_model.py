import os, signal
import physics
from subprocess import Popen

def run(setup, replay_speed = 1, accuracy = 5, total_time = 100, start_server=False):
    if start_server:
        os.setpgrp()  # create new process group, become its leader
        try:
            Popen(["bash", "./start.sh"])
            __run(setup, replay_speed, accuracy, total_time)
        finally:
            os.killpg(0, signal.SIGKILL)  # kill all processes in my group
    else:
        __run(setup, replay_speed, accuracy, total_time)


def __run(setup, replay_speed, accuracy, total_time):
    timestep = 1/(10**accuracy)
    sim_step = 10**(accuracy-1)
    u = physics.Universe(timestep)
    setup(u)

    fl = open("data.txt", "w")
    while u.time <= total_time:
            u.infolog()
            d = str(u.data())
            d += '\n'
            fl.write(d)
            fl.flush()
            for i in range(sim_step):
                u.step()
