'''
Created on Feb 18, 2010

altered on Feb. 20, 2014
'''

from struct import pack
from sys import maxint, exit

#create new account
def create_request(conn):
    
    print "CREATING AN ACCOUNT \n"
    print "enter a starting balance:"
	buffer = new message_pb2.User
	buffer.version_num = 'x\01'
	buffer.opcode = 'x\10'
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        if(netBuffer >= 0 and netBuffer < maxint):
            buffer.bal = netbuffer
            break
        
    print "enter a an account number 1-100(input 0 for a random number):"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
			buffer.account_num = netBuffer
            break
        elif(netBuffer == 0):
            act = -1
            break
    
	send_buffer(buffer, conn)
    return

#delete an existing account
def delete_request(conn):
    print "DELETING AN ACCOUNT \n"
	buffer = new message_pb2.User
	buffer.version_num = 'x\01'
	buffer.opcode = 'x\20'
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            buffer.account_num = netBuffer
            break

    send_buffer(buffer, conn)
    return

#deposit to an existing account
def deposit_request(conn):
    print "DEPOSITING SOME DOUGH \n"
	buffer = new message_pb2.User
	buffer.version_num = 'x\01'
	buffer.opcode = 'x\30'
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            buffer.account_num = netbuffer
            break
    print "enter an amount to deposit:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        if(netBuffer >= 0 and netBuffer < maxint):
            buffer.bal = netbuffer
            break
	
    send_buffer(buffer, conn)
	return

#withdraw from an existing account
def withdraw_request(conn):
    print "WITHDRAWING SOME DOUGH \n"
	buffer = new message_pb2.User
	buffer.version_num = 'x\01'
	buffer.opcode = 'x\40'
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            buffer.account_num = netbuffer
            break
        
    print "enter an amount to withdraw:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        if(netBuffer >= 0 and netBuffer < maxint):
            buffer.bal = netbuffer
            break
    
	send_buffer(buffer, conn)
	return

#withdraw from an existing account
def balance_request(conn):
    print "CHECKING THE BALANCE OF AN ACCOUNT \n"
	buffer = new message_pb2.User
	buffer.version_num = 'x\01'
	buffer.opcode = 'x\50'
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            buffer.account_num = netBuffer
            break

    send_buffer(buffer, conn)
    return

#end a session
def end_session(conn):
	buffer = new message_pb2.User
	buffer.version_num = 'x\01'
	buffer.opcode = 'x\60'
    send_buffer(buffer, conn)
    return

def send_message(message, conn):
    try:
        conn.send(message)
    except:
            #close the client if the connection is down
            print "ERROR: connection down"
            exit()
    return

#function to encrypt message and create a hash and then send it to the server
def send_buffer(buffer, conn):
    buffer.checksum = md5.new(buffer.SerializeToString)
	buffer_string = buffer.SerializeToString
	length = len(buffer_string)
	send_message(pack('!I', length),conn)
	send_message(buffer_string, conn)
	return