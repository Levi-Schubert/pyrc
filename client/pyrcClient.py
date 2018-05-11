# PyRC Client [Version 0.1.0]
# Author: Levi Schubert [me@Levischubert.com]
# Description: A python client to send and receive chat messages with its corresponding server
# Date: 4/25/18

import socket
import _thread
# import cryptography
import time

global command
global connected
global name
global sock
name = ""
connected = False

def help():
	print("-------------------------HELP MENU-----------------------------")
	print("commands:")
	print("connect | opens the connection menu")
	print("setName | opens the username settings")
	print("chat	| attempts to connect to the chat of the current server")
	print("help	| opens this help page")
	print("exit	| terminates the program")

def connect():
	global command
	global connected
	global host
	global sock
	# answer = ""
	# if(host != None){
	# 	print("Would you like to use the previous hostname? (y/n)")
	# 	answer = input()
	# }
	# if(answer == "y"){
	# 	connected = True
	# 	print("The connected host is: " + host)	
	# }else{
	# 	print("Enter hostname for server to connect to: ")
	# 	host = input()
	# 	connected = True
	# }
	# sock = socket.socket()
	connected = True
	sock = socket.socket()
	# host = "pyrc.tk"
	# host = socket.gethostname()
	host = "127.0.0.1"

def setName():
	global name
	name = input("Please choose a username to be displayed on servers: ")
	print("Your username has been set to: " + name)

def printChat(sock, dont):
	while True:
		data = sock.recv(1024).decode()
		if not data:
			chatting = False
			break
		print(data)


def chat():
	global connected
	global name
	global chatting
	global sock
	chatting = True
	counter = 0
	if connected == False:
		print("Error: you are not connected to a server")
	elif(name == ""):
		print("Error: you have not set a username")
	else:
		print("System: You are now chatting with the server. Use /exit to leave the chat.")
		sock.connect((host,7972))
		_thread.start_new_thread(printChat, (sock, None))
		sock.send(name.encode())
		while(chatting):
			arg = input()
			if(arg.split(' ',1)[0] == "/exit"):
				chatting = False
				print("You're now disconnected from the chat")
			else:
				print("\033[A																				\033[A")
				sock.send(arg.encode())
				# sock.send(("message number: " + str(counter)).encode() )
				# counter += 1
	sock.close()
	connected = False
			#parse input to send chat

def createUserConfig():
	NotImplemented

def createUser():
	NotImplemented
	createUserConfig()

def onClose():
	NotImplemented

def login():
	NotImplemented

def interpret(com):
	cmd = com.split(' ', 1)[0]
	if cmd == "connect":
		connect()
	elif cmd == "help":
		help()
	elif cmd == "setName":
		setName()
	elif cmd == "chat":
		chat()
	else:
		print("Error: unrecognized command, type 'help' for a list of commands")


def main():
	global command
	print("Welcome to PyRC [Version 0.1.0]")
	print("Type 'help' to get started")
	print("User Test version usage:")
	print("type 'setName' and follow the prompt to set a username")
	print("type connect | The ip and port are already set for the test")
	print("type chat to enter the chat room and connect")
	command = input()
	while(command != "exit"):
		interpret(command)
		command = input()
	print("thanks for using PyRC")
	SystemExit


main()