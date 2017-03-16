#!/usr/bin/python

#Type a command to send it to the entire network
#Commands send to Ethernet Link devices should start with "^^Id"
#Commands sent to the underlying Whozz Calling? whould start with "^^Id-"
from socket import *
import time, threading

class ListenThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.alive = False
    def run (self):
        host = "0.0.0.0"
        port = 3520
        buffer = 202400

        UDPSock = socket(AF_INET,SOCK_DGRAM) #Socket Datagram
        UDPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        UDPSock.bind((host,port))
        time.clock()
        print "-" * 40
        print "Starting Server\nType a command, then press enter to broadcast that command\n\n"
        self.alive = True
        while self.alive:
            try:
                data,addr = UDPSock.recvfrom(buffer)
                if not data:
                    print "No data."
                    break
                elif "quit" in data:
                    print "Quitting..."
                    break
                else:
                    donestamp = time.clock()
                    
                    if data.rfind("$"):
                        data = data[data.rfind("$"):]
                        print "--------------------"
                        print " Non-hex:\n"
                        print data
                        print "----------"
                        data = ":".join("{0:x}".format(ord(c)) for c in data)
                        print "Hex:\n"
                        print data
                        
            except (KeyboardInterrupt, SystemExit):
                raise
                UDPSock.close()
            except:
                traceback.print_exc()

    def finish(self):
        self.alive = False
            

Listen = ListenThread()
Listen.start()

host = "255.255.255.255"
port = 3520
UDPSock = socket(AF_INET,SOCK_DGRAM) #Socket Datagram
UDPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
UDPSock.bind(('',port)) # important addition to force sour/dest ports to 3520 (1/17/14)
time.sleep(.001)
while 1:
    try:
        data = raw_input('')
        UDPSock.sendto(data,(host,port))
    except:
        UDPSock.sendto("quit",(host,port))
        Listen.finish()
        break
