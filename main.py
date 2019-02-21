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
	univ[request.sid] = physics.Universe(forces=[physics.GravityForce])
	
@socketio.on('particle')
def create_particle(pos, vel, mass):
	p = physics.Particle(pos, vel, mass)
	univ[request.sid].add(p)

@socketio.on('step')
def take_step():
	# TODO: Isn't this wrong?
	# Putting a blocking operation in the main thread
	# How do I fix this?
	univ[request.sid].step()

@socketio.on('data')
def send_data():
	return univ[request.sid].data()

if __name__ == '__main__':
	socketio.run(app, port=5000, debug=True)
