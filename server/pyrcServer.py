# PyRC Server [Version 0.1.0]
# Author: Levi Schubert [me@levischubert.com]
# Description: a Python Relay Chat server lightweight enough to run on a Raspberry Pi
#              with AES data encryption
# Date: 4/25/18

import time
import _thread
#import cryptography
import socket

#global variables
global messages
global index

messages = []
index = 0

#remove the previous thousand messages from the buffer and save to a log file
def clearOld():
	global messages
	with open("log.txt", "a") as log:
		for msg in messages:
			log.write(msg)
	

def addMessage(msg):
	global messages
	global index
	if(index > 1000):
		clearOld()
		messages = []
		index = -1
	messages.append(msg)
	index += 1
	# print("added '" + msg + "' to global array")

def sendChat(conn, localIndex):
	while True:
		if(localIndex != index):
			conn.send(messages[localIndex].encode())
			localIndex += 1
			if(localIndex >= 1000):
				localIndex = 0

def handling(conn, addr):
	global index
	global messages
	global userCount
	localIndex = index
	user = conn.recv(1024).decode()
	_thread.start_new_thread(sendChat, (conn, localIndex))
	# print("thread for " + user + " starting loop")
	while True:
		data = conn.recv(1024).decode()
		if not data:
			break
		print('[' + time.strftime('%H:%M') + '] ' + user + ": " + str(data))
		if(data != None):
			data = (user + ': ' + str(data))
			addMessage(data)
			# localIndex += 1
		# sendData = messages[localIndex]
		# print('[' + time.strftime('%H:%M') + "] sending " + str(data).upper())
		# print("sending: '" + sendData + "' to " + user)
		# conn.send(sendData.encode())
	conn.close()
	print('[' + time.strftime('%H:%M') + '] ' + str(addr) + " disconnected; Closing Thread")
	

def thread():
	host = "192.168.1.142"
	# host = "127.0.0.1" #local host for debugging and development
	port = 7972
	print("server started on: " + host + ":" + str(port))
	mySocket = socket.socket()
	mySocket.bind((host,port))

	while True:
		mySocket.listen(1)
		conn, addr = mySocket.accept()
		_thread.start_new_thread(handling, (conn, addr))
		print('[' + time.strftime('%H:%M') + "] New thread created for connection from: " + str(addr))
	mySocket.close()

def main():
	thread()

main()
exit(-1)

