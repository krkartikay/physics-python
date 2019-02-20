"""
Server Backend
"""

import physics

from flask import *
from flask_socketio import SocketIO

# u = physics.Universe(forces=[physics.GravityForce])

# p = physics.Particle((0,0,0), (1,0,10), 1)

# u.add(p)

# while p.pos.xyz[2] >= 0:
# 	print("%0.3f"%u.time, p.pos)
# 	u.step()

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
	univ[request.sid].step()

@socketio.on('data')
def send_data():
	return univ[request.sid].data()

if __name__ == '__main__':
	socketio.run(app, port=5000, debug=True)
