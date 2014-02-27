'''
CS 262: Distributed Systems

Created on Feb 18, 2010

Restructured and re-factored by Jim Waldo, 2/17/2014
'''

import socket
import struct
from myServerReceive import opcodes
import myServerSend
from myServerSend import unknown_opcode
import thread

# Import the interface to our GPB messages
import sys
sys.path.append('./..')
import messages_pb2

import hashlib
def verify_checksum(message):
  received_checksum = message.checksum
  message.checksum = ''
  computed_checksum = hashlib.sha256(message.SerializeToString()).digest()
  message.checksum = received_checksum
  return received_checksum == computed_checksum

version = '\x01'

def recordConnect(log, addr):
    print 'Opened connection with ' + addr
    log.write('Opened connection with ' + addr + '\n')
    log.flush()
    
#thread for handling clients
def handler(conn,lock, myData):
  #keep track of erroneous opcodes
  second_attempt = 0
  while True:   
    #retrieve header
    try:
        netbuffer = conn.recv( 1024 )
    except:
        #close the thread if the connection is down
        thread.exit()
    #if we receive a message...
    if len(netbuffer) >= 4:
      # Get the GPB message length
      length = struct.unpack('!I',netbuffer[0:4])[0]
      
      if len(netbuffer) == 4:
        # Only received the length so far
        netbuffer += mySocket.recv( 1024 )
      
      #only allow correct version numbers and buffers that are of the appropriate length
      if (len(netbuffer) == (length + 4)):
        # Populate the message with the data received
        message = messages_pb2.ClientRequest()
        message.ParseFromString(netbuffer[4:4+length])
        if (message.version== version) and verify_checksum(message):
          opcode = message.opcode
          #try to send packet to correct handler
          try:
            opcodes[opcode](conn,message,myData,lock)
          #catch unhandled opcodes
          except KeyError:
            if(second_attempt):
              #disconnect the client
              myServerSend.end_session_success(conn)
              conn.close()
              return
            else:
              #send incorrect opcode message
              second_attempt = 1
              unknown_opcode(conn)


if __name__ == '__main__':
    #set up log
    log = open('log.txt', 'a')
    #data structure for storing account information
    myData = dict()

    #setup socket
    mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    mySocket.bind(('',8080))
    mySocket.listen(5)  #param represents the number of queued connections

    #listening for connections
    try:
      while True:
          #This is the simple way to start this; we could also do a SELECT
          conn, address = mySocket.accept()
          #log connection
          recordConnect(log, str(address)) 
          #start a new thread
          lock = thread.allocate_lock()
          thread.start_new_thread(handler, (conn, lock, myData))
    except:
      mySocket.close()
      
    log.close()