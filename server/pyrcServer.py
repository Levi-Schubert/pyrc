# PyRC Server [Version 0.0.2]
# Author: Levi Schubert [me@levischubert.com]
# Description: a Python Relay Chat server lightweight enough to run on a Raspberry Pi
#              with AES data encryption
# Date: 4/25/18

import time
import _thread
#import cryptography
import socket

def handling(conn, addr):
    user = conn.recv(1024).decode()
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print('[' + time.strftime('%H:%M') + '] ' + user + ": " + str(data))
        data = (user + ': ' + str(data))
        #data = str(data).upper()
        print('[' + time.strftime('%H:%M') + "] sending " + str(data).upper())
        conn.send(data.encode())
    print('[' + time.strftime('%H:%M') + '] ' + str(addr) + " disconnected; Closing Thread")
    conn.close()

def thread():
    #host = "192.168.1.130"
    host = "192.168.1.135" #local host for debugging and development
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

