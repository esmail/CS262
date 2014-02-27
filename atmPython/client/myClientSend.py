'''
Created on Feb 18, 2010

altered on Feb. 20, 2014
'''

from struct import pack
from sys import maxint, exit

# Import the interface to our GPB messages
import sys
sys.path.append('./..')
import messages_pb2

sys.path.append('./../server')
from myServerSend import insert_checksum

# create new account
def create_request(conn):
  print "CREATING AN ACCOUNT \n"
  print "enter a starting balance:"
  message = messages_pb2.ClientRequest()
  message.version = '\x01'
  message.opcode = '\x10'
  while True:
    try:
      netBuffer = int(raw_input('>> '))
    except ValueError:
      continue
    if(netBuffer >= 0 and netBuffer < maxint):
      message.bal = netBuffer
      break
    
  print "enter a an account number 1-100(input 0 for a random number):"
  while True:
    try:
      netBuffer = int(raw_input('>> '))
    except ValueError:
      continue
      
    if(netBuffer > 0 and netBuffer <= 100):
      message.act = netBuffer
      break
    elif(netBuffer == 0):
      message.act = -1
      break
  
  send_buffer(message, conn)
  return

# delete an existing account
def delete_request(conn):
  print "DELETING AN ACCOUNT \n"
  message = messages_pb2.ClientRequest()
  message.version = '\x01'
  message.opcode = '\x20'
  print "enter a an account number 1-100:"
  while True:
      try:
          netBuffer = int(raw_input('>> '))
      except ValueError:
          continue
      
      if(netBuffer > 0 and netBuffer <= 100):
          message.act = netBuffer
          break
  
  send_buffer(message, conn)
  return

# deposit to an existing account
def deposit_request(conn):
  print "DEPOSITING SOME DOUGH \n"
  message = messages_pb2.ClientRequest()
  message.version = '\x01'
  message.opcode = '\x30'
  print "enter a an account number 1-100:"
  while True:
    try:
        netBuffer = int(raw_input('>> '))
    except ValueError:
        continue
    
    if(netBuffer > 0 and netBuffer <= 100):
        message.act = netBuffer
        break
  print "enter an amount to deposit:"
  while True:
    try:
        netBuffer = int(raw_input('>> '))
    except ValueError:
        continue
    if(netBuffer >= 0 and netBuffer < maxint):
        message.bal = netBuffer
        break
  
  send_buffer(message, conn)
  return

# withdraw from an existing account
def withdraw_request(conn):
  print "WITHDRAWING SOME DOUGH \n"
  message = messages_pb2.ClientRequest()
  message.version = '\x01'
  message.opcode = '\x40'
  print "enter a an account number 1-100:"
  while True:
    try:
        netBuffer = int(raw_input('>> '))
    except ValueError:
        continue
    
    if(netBuffer > 0 and netBuffer <= 100):
        message.act = netBuffer
        break
    
  print "enter an amount to withdraw:"
  while True:
    try:
        netBuffer = int(raw_input('>> '))
    except ValueError:
        continue
    if(netBuffer >= 0 and netBuffer < maxint):
        message.bal = netBuffer
        break
  
  send_buffer(message, conn)
  return

# withdraw from an existing account
def balance_request(conn):
  print "CHECKING THE BALANCE OF AN ACCOUNT \n"
  message = messages_pb2.ClientRequest()
  message.version = '\x01'
  message.opcode = '\x50'
  print "enter a an account number 1-100:"
  while True:
    try:
        netBuffer = int(raw_input('>> '))
    except ValueError:
        continue
    
    if(netBuffer > 0 and netBuffer <= 100):
        message.act = netBuffer
        break
  
  send_buffer(message, conn)
  return

# end a session
def end_session(conn):
  message = messages_pb2.ClientRequest()
  message.version = '\x01'
  message.opcode = '\x60'
  send_buffer(message, conn)
  return
  
def send_message(message, conn):
  try:
    conn.send(message)
  except:
        # close the client if the connection is down
        print "ERROR: connection down"
        exit()
  return

# function to encrypt message and create a hash and then send it to the server
def send_buffer(message, conn):
  insert_checksum(message)
  message_string = message.SerializeToString()
  length = len(message_string)
  send_message(pack('!I', length)+message_string, conn)
  return
