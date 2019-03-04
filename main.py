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

@socketio.on('connect')
def on_connect():
	univ[request.sid] = physics.Universe()
	univ[request.sid].addForce(physics.GravityForce())
	univ[request.sid].addForce(physics.DragForce())
	univ[request.sid].addForce(physics.SpringForce())

@socketio.on('init')
def on_init():
	p1 = physics.FixedParticle((0, 0, 5), (0, 0, 0), 1)
	p2 = physics.Particle((0, 0, 0), (2, 0, 2), 1)
	s1 = physics.Spring(p1, p2, k=100, damping=10)
	univ[request.sid].add(p1)
	univ[request.sid].add(p2)
	univ[request.sid].add(s1)

@socketio.on('particle')
def create_particle(pos, vel, mass):
	p = physics.Particle(pos, vel, mass)
	univ[request.sid].add(p)

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
