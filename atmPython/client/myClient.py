'''
Created on Feb 18, 2010

Altered Feb. 20, 2014
'''

version = '\x01'

import socket
from myClientSend import *
from myClientReceive import opcodes
import sys
import struct

# Import the interface to our GPB messages
sys.path.append('./..')
import messages_pb2

from myServer import verify_checksum


def getInput():
    print '''
CONNECTED TO ATM SERVER - type the number of a function:
    (1) Create Account
    (2) Delete Account
    (3) Deposit Money to an Account
    (4) Withdraw Money from an Account
    (5) Check the Balance of an Account
    (6) End Session
    '''
    netBuffer = raw_input('>> ')
    return netBuffer

def processInput(netBuffer, mySocket):
    request_serviced = True
    
    #create
    if netBuffer == str(1):
        create_request(mySocket)
        
    #delete
    elif netBuffer == str(2):
        delete_request(mySocket)
        
    #deposit
    elif netBuffer == str(3):
        deposit_request(mySocket)
        
    #withdraw
    elif netBuffer == str(4):
        withdraw_request(mySocket)
        
    #balance
    elif netBuffer == str(5):
        balance_request(mySocket)
        
    #quit
    elif netBuffer == str(6):
        end_session(mySocket)
    
    else:
      request_serviced = False
        
    return request_serviced
        
def getResponse(mySocket):
    #wait for server responses...
    while True:
        try:
            retBuffer = mySocket.recv( 1024 )
        except:
            #close the client if the connection is down
            print "ERROR: connection down"
            sys.exit()
            
        if len(retBuffer) >= 4:
          # Get the GPB message length
          length = struct.unpack('!I',retBuffer[0:4])[0]
          
          if len(retBuffer) == 4:
            # Only received the length so far
            retBuffer += mySocket.recv( 1024 )
            
          if (len(retBuffer) == (length + 4)):
            # Populate the message with the data received
            message = messages_pb2.ServerResponse()
            message.ParseFromString(retBuffer[4:4+length])
            #only allow correct version numbers
            if (message.version== version) and verify_checksum(message):
                opcode = message.opcode
                #send packet to correct handler
                try:
                    opcodes[opcode](mySocket,message)
                except KeyError:
                    break
            #mySocket.send ('\x01\x01\x02\x03\x53\x10\x12\x34')
            break
        return
    
if __name__ == '__main__':
    if(len(sys.argv) != 3):
      # Use defaults
      myHost = 'localhost'
      myPort = '8080'
#         print "ERROR: Usage 'python myClient.py <host> <port>'"
#         sys.exit()
    else:    
    #get the address of the server
      myHost = sys.argv[1]
      myPort = sys.argv[2]
      
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #mySocket.settimeout(5.)
    try:
      mySocket.connect ( ( myHost, int(myPort)) )
    except:
      print "ERROR: could not connect to " + myHost + ":" + myPort
      sys.exit()

    while True:
      netBuffer = getInput()
      #menu selection and function priming
      if (processInput(netBuffer, mySocket)):
        getResponse(mySocket)

    mySocket.close()