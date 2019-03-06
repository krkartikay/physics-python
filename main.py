"""
Server Backend
"""

import physics

from flask import *
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

univ = {}
f = []
f_reqs = 0

@socketio.on('init')
def init_physics(timestep=0.001):
	univ[request.sid] = physics.Universe(timestep=timestep)
	return 1

@socketio.on('reload_file')
def reload_file():
	global f
	f = open("data.txt").readlines()
	return 1

@socketio.on('add_force')
def add_force(forcename, options={}):
	force = getattr(physics, forcename)
	univ[request.sid].addForce(force(**options))

@socketio.on('ping')
def ping(*data):
	return "pong: " + str(data)

@socketio.on('particle')
def create_particle(pos, vel, mass):
	p = physics.Particle(pos, vel, mass)
	return univ[request.sid].add(p) # returns particle id

@socketio.on('fixed_particle')
def create_fixed_particle(pos, mass):
	p = physics.FixedParticle(pos, (0,0,0), mass)
	return univ[request.sid].add(p)  # returns particle id

@socketio.on('spring')
def create_spring(pid1, pid2, options={}):
	p1 = univ[request.sid].objects[pid1]
	p2 = univ[request.sid].objects[pid2]
	sp = physics.Spring(p1, p2, **options)
	return univ[request.sid].add(sp)  # returns spring id

@socketio.on('impulse')
def create_impulse(pid, options={}):
	p = univ[request.sid].objects[pid]
	p.connections += [physics.Impulse(**options)]

@socketio.on('step')
def step_num(num=1):
	for i in range(num):
		# TODO: Should this be done in the background?
		univ[request.sid].step()
	return True

@socketio.on('data')
def send_data():
	return univ[request.sid].data()

@socketio.on('saved_data')
def send_saved_data(i):
	global f
	i -= 30
	if i < 0:
		i = 0
	if i>=len(f):
		f = open("data.txt").readlines()
		return "restart"
	else:
		return eval(f[i])

if __name__ == '__main__':
	socketio.run(app, port=5000, debug=True)
