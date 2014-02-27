'''
Created on Feb 18, 2010

Altered Feb 20, 2014
'''

import struct

import hashlib
# Import the interface to our GPB messages
import sys
sys.path.append('./..')
import messages_pb2

def insert_checksum(message):
  message.checksum = ''
  message.checksum = hashlib.sha256(message.SerializeToString()).digest()


def general_failure(conn, err_type, reason):
    
    #find the appropriate opcode to send for particular errors
    if err_type == 'create':
        typebyte = '\x12'
    elif err_type == 'delete':
        typebyte = '\x22'
    elif err_type == 'deposit':
        typebyte = '\x32'
    elif err_type == 'withdraw':
        typebyte = '\x42'
    elif err_type == 'balance':
        typebyte = '\x52'
    
    # Create a message to be transmitted
    message = messages_pb2.ServerResponse()
    message.version = '\x01'
    message.opcode = typebyte
    message.error_message = reason.encode('utf-8')
    insert_checksum(message)
    
    # Send
    message_string = message.SerializeToString()
    length = len(message_string)
    
    conn.send(struct.pack('!I',length))
    conn.send(message_string)
    return

#create new account
def create_success(conn,act):
    # Create a message to be transmitted
    message = messages_pb2.ServerResponse()
    message.version = '\x01'
    message.opcode = '\x11'
    message.act = act
    insert_checksum(message)
    
    # Send
    message_string = message.SerializeToString()
    length = len(message_string)
    conn.send(struct.pack('!I',length))
    conn.send(message_string)
    return

#delete an existing account
def delete_success(conn):
    conn.send('\x01\x00\x00\x00\x00\x21')
    # Create a message to be transmitted
    message = messages_pb2.ServerResponse()
    message.version = '\x01'
    message.opcode = '\x21'
    insert_checksum(message)
    
    # Send
    message_string = message.SerializeToString()
    length = len(message_string)
    conn.send(struct.pack('!I',length))
    conn.send(message_string)
    return

#deposit to an existing account
def deposit_success(conn,bal):
    # Create a message to be transmitted
    message = messages_pb2.ServerResponse()
    message.version = '\x01'
    message.opcode = '\x31'
    message.bal = bal
    insert_checksum(message)
    
    # Send
    message_string = message.SerializeToString()
    length = len(message_string)
    conn.send(struct.pack('!I',length))
    conn.send(message_string)
    return

#withdraw from an existing account
def withdraw_success(conn,bal):
    # Create a message to be transmitted
    message = messages_pb2.ServerResponse()
    message.version = '\x01'
    message.opcode = '\x41'
    message.bal = bal
    insert_checksum(message)
    
    # Send
    message_string = message.SerializeToString()
    length = len(message_string)
    conn.send(struct.pack('!I',length))
    conn.send(message_string)
    return

#withdraw from an existing account
def balance_success(conn,bal):
    # Create a message to be transmitted
    message = messages_pb2.ServerResponse()
    message.version = '\x01'
    message.opcode = '\x51'
    message.bal = bal
    insert_checksum(message)
    
    # Send
    message_string = message.SerializeToString()
    length = len(message_string)
    conn.send(struct.pack('!I',length))
    conn.send(message_string)
    return

#end a session
def end_session_success(conn):
    # Create a message to be transmitted
    message = messages_pb2.ServerResponse()
    message.version = '\x01'
    message.opcode = '\x61'
    insert_checksum(message)
    
    # Send
    message_string = message.SerializeToString()
    length = len(message_string)
    conn.send(struct.pack('!I',length))
    conn.send(message_string)
    return

#handle invalid opcodes
def unknown_opcode(conn):
    # Create a message to be transmitted
    message = messages_pb2.ServerResponse()
    message.version = '\x01'
    message.opcode = '\x62'
    insert_checksum(message)
    
    # Send
    message_string = message.SerializeToString()
    length = len(message_string)
    conn.send(struct.pack('!I',length))
    conn.send(message_string)
    return
  