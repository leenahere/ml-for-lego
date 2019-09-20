#!/usr/bin/python
# -*- coding: utf-8 -*-

from socket import *
from threading import Thread, Lock
import sys

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# IP of robot
server_ip = str(sys.argv[1])

# port to connect to
server_port = 50007

# currently pressed Keys
pressed_keys = []

# Keys allowed to press
allowed_keys = ['a', 'w', 's', 'd']

# array which will be sent
array_to_send = [0, 0, 0, 0]

# function to lock area before it is used by thread
lock = Lock()

keep_running = True

def running():
    return keep_running


# array of bools to encode string
def to_binary(num_list):
    bin = ''
    # get every item from array and add it to string
    for i in num_list:
        bin = bin + str(i)
    # return encode string
    return bin.encode()

class my_handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global keep_running
        if self.path[8] == '1':
            keep_running = False
        else:
            if self.path[0:3] == '/?c':
                global array_to_send
                lock.acquire()
                array_to_send = [self.path[4], self.path[5], self.path[6], self.path[7]]
                lock.release()
            else:
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                f = open("index.html", "r")
                self.wfile.write(str(f.read()))
        return


def web_server():
    server = HTTPServer(('', 8080), my_handler)
    while running():
        server.handle_request()

    return


# connect to server and send control signals
def connect_to_server():
    # connect to the server
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((server_ip, server_port))

    # set reference array to compare that the client only sends by changes
    global array_to_send
    lastSend = array_to_send[:]

    while thread_keys.isAlive():
        # lock before entering area
        lock.acquire()
        # check for changes
        if not array_to_send == lastSend:
            # send to server
            s.send(to_binary(array_to_send))
            # copy input of array to reference array
            lastSend = array_to_send[:]
        # release area
        lock.release()

    # close connecton to server
    s.close()


# init threads for key listener and sender
thread_keys = Thread(target=web_server)
thread_server = Thread(target=connect_to_server)

if __name__ == "__main__":
    # start threads
    thread_keys.start()
    thread_server.start()
