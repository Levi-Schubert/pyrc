import socket
import threading
import datetime

# File: pyrc_server
# Version: 0.0.1
# Description: A python server to handle the incoming connections and data from its corresponding client and to
#              send the messages to all connected users
# Author: Levi Schubert

sock = socket.socket()
host = socket.gethostname()
port = 7000
sock.bind((host, port))


sock.listen(5)
while True:
    connection, origin = sock.accept()
    message = sock.recv()
    print("[" + datetime + "] " + origin + ": " + message)
    connection.send(message)
    connection.close()

