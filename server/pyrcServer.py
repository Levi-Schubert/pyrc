# PyRC Server [Version 0.1.0]
# Author: Levi Schubert [me@levischubert.com]
# Description: a Python Relay Chat server lightweight enough to run on a Raspberry Pi
#			   with AES data encryption
# Date: 4/25/18

import time
import _thread
from Crypto.Cipher import AES
import socket
import configparser
import sys
import getpass
from io import StringIO

#global variables
global messages
global index
global running
global logging
global user
global loginCipher

#assigning initial global variables
running = False
logging = False
loginCipher = AES.new("default pyrc server login cipher", AES.MODE_CBC, 'default pyrc IV0')

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

def showLog():

	localIndex = index
	while logging:
		if(localIndex != index):
			print('[' + time.strftime('%H:%M') + '] ' + messages[localIndex])
			localIndex += 1
			if(localIndex >= 1000):
				localIndex = 0


def sendChat(conn, localIndex):
	while running:
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
	while running:
		data = conn.recv(1024).decode()
		if not data:
			break
		# print('[' + time.strftime('%H:%M') + '] ' + user + ": " + str(data))
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
	global running
	# host = "192.168.1.142"
	host = "127.0.0.1" #local host for debugging and development
	port = 7972
	# print("server started on: " + host + ":" + str(port))
	mySocket = socket.socket()
	mySocket.settimeout(5)
	mySocket.bind((host,port))
	print('[' + time.strftime('%H:%M') + "] Server started on: " + host + ":" + str(port))
	while running:
		try:
			mySocket.listen(1)
			conn, addr = mySocket.accept()
			_thread.start_new_thread(handling, (conn, addr))
			print('[' + time.strftime('%H:%M') + "] New thread created for connection from: " + str(addr))
		except Exception as err:
			pass
	mySocket.close()
	print('[' + time.strftime('%H:%M') + "] Closing server at: " + host + ":" + str(port))

def newUser():
	global user
	user = input("new username: ")
	config = configparser.ConfigParser()
	config.read("users.ini")
	config[user] = {}
	with open('users.ini', 'w') as configfile:
			config.write(configfile)
	setPass()
	

def setPass():
	global user
	global loginCipher
	password = getpass.getpass(prompt="type  new  password: ", stream=None)
	confirm = getpass.getpass(prompt="confirm new password: ", stream=None)
	if(password == confirm):
		config = configparser.RawConfigParser()
		config.read("users.ini")
		config[user] ["password"] = str(loginCipher.encrypt(pad(password)))
		with open('users.ini', 'w') as configfile:
			config.write(configfile)
	else:
		print("passwords didn't match, password change not applied")
	NotImplemented

def pad(string):
	while(not len(string)%16 == 0):
		string += chr(124)
	return string


def interpret(com):
	global running
	global logging
	if(com == "init" and running != True):
		running = True
		_thread.start_new_thread(thread, ())
	elif(com == "init" and running == True):
		print("Server already running")
	elif(com == "close"):
		running = False
	elif(com == "toggleLog"):
		if(logging):
			logging = False
		else:
			logging = True
			_thread.start_new_thread(showLog, ())
	elif(com == "newUser"):
		newUser()
	elif(com == "setPass"):
		setPass()
		
def login():
	global user
	global loginCipher
	print("Login to PyRC Server")
	username = input("Username: ")
	config = configparser.RawConfigParser()
	config.read("users.ini")
	if(username in config):
		password = getpass.getpass(prompt="password: ", stream=None)
		if((config[username]["password"]) == password):
			print("successfully logged in")
			print("[  NOTICE  | YOUR PASSWORD IS STORED IN PLAIN TEXT]")
			print("[use 'setPass' to change and encrypt your password]")
			user = username
			return True
		elif((config[username]["password"]) == str(loginCipher.encrypt(pad(password)))):
			print("successfully logged in")
			user = username
			return True
		print((config[username]["password"]) + " vs " + str(loginCipher.encrypt(pad(password))))
		print("[incorrect password or username, exiting system]")
	return False

def main():
	print("|PyRC Server [Version 0.1.0]|")
	global user
	if(login()):
		command = input
		while(command != "exit"):
			interpret(command)
			command = input(user + " ➤ ")
	

main()
exit(-1)

