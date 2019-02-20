"""
Server Backend
"""

import physics

from flask import Flask
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

@socketio.on('join')
def on_join(data):
	print("YES")

if __name__ == '__main__':
	socketio.run(app, port=5000, debug=True)
