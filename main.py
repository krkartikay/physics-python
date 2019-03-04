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

@socketio.on('init')
def init_physics(forces, timestep=0.001):
	univ[request.sid] = physics.Universe(timestep=timestep)
	for f in forces:
		if isinstance(f, list):
			args = f[1]
			f = f[0]
		else:
			args = {}
		try:
			f = getattr(physics, f)
			univ[request.sid].addForce(f(**args))
		except AttributeError:
			return "Failed"

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
def create_spring(pid1, pid2, options):
	p1 = univ[request.sid].objects[pid1]
	p2 = univ[request.sid].objects[pid2]
	sp = physics.Spring(p1, p2, **options)
	return univ[request.sid].add(sp)  # returns spring id

@socketio.on('step')
def take_step():
	# TODO: Should this be done in the background?
	univ[request.sid].step()

@socketio.on('step')
def step_num(num):
	for i in range(num):
		univ[request.sid].step()

@socketio.on('data')
def send_data():
	return univ[request.sid].data()

if __name__ == '__main__':
	socketio.run(app, port=5000, debug=True)
