#! /usr/bin/env python3

from socket import *
from ev3dev.ev3 import *

echo_port = 50007
buf_size = 1024


right = Motor('outC')
left = Motor('outB')


def control_engine(instructions):
    if instructions == '0100':
        right.run_forever(speed_sp=100)
        left.run_forever(speed_sp=100)
    elif instructions == '1000':
        right.run_forever(speed_sp=100)
        left.run_forever(speed_sp=0)
    elif instructions == '0001':
        right.run_forever(speed_sp=0)
        left.run_forever(speed_sp=100)
    elif instructions == '1100':
        right.run_forever(speed_sp=100)
        left.run_forever(speed_sp=30)
    elif instructions == '0101':
        right.run_forever(speed_sp=30)
        left.run_forever(speed_sp=100)
    elif instructions == '0010':
        right.run_forever(speed_sp=-100)
        left.run_forever(speed_sp=-100)
    else:
        right.run_forever(speed_sp=0)
        left.run_forever(speed_sp=0)


def server():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', echo_port))
    s.listen(1)

    print('server is up')

    conn, (remote_host, remote_port) = s.accept()
    print('connected with ' + str(remote_host) + ':' + str(remote_port))

    while 1:
        data = conn.recv(buf_size)
        control_engine(str(data)[-5:-1])

        if not data:
            break

    print('connection is closed')
    control_engine('0000')
    s.close()


if __name__ == "__main__":
    server()
