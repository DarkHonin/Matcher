from app import app, sockets

sockets.run(app, host="0.0.0.0")

