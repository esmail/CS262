'''
Created on Feb 18, 2010

Altered Feb. 20, 2014
'''
from sys import exit


# Repackage our GPB message into a list of values so we can reuse this code with only minor modification
def repackage_message(message):
  values = list()
  
  # Use a slightly weird method of referencing opcodes by the functions that handle them so the code is less opaque
  if opcodes[message.opcode] in [delete_success, end_session_success, unknown_opcode]:
    # These messages have no additional data so return an empty list
    None
    
  elif opcodes[message.opcode] == create_success:
    values.append(message.act)
    
  elif opcodes[message.opcode] == general_failure:
    values.append(message.error_message)
    
  # All other server responses include the balance only
  else:
    values.append(message.bal)
  
  return values

#handle errors from server side.
def general_failure(conn, message):
  # No shortcut here  
  print "\nERROR: " + message.error_message
  return

#create new account
def create_success(conn, message):
    values = repackage_message(message)
    print "Account creation successful " + str(values[0])
    return

#delete an existing account
def delete_success(conn, message):
    print "Account deletion successful"
    return

#deposit to an existing account
def deposit_success(conn,message):
    values = repackage_message(message)
    print "Deposit success. The updated balance: " + str(values[0])
    return

#withdraw from an existing account
def withdraw_success(conn,message):
    values = repackage_message(message)
    print "Withdrawal success. The updated balance: " + str(values[0])
    return

#withdraw from an existing account
def balance_success(conn,message):
    values = repackage_message(message)
    print "The balance of that account is: " + str(values[0])
    return

#end a session
def end_session_success(conn,message):
    print "SHUTTING DOWN"
    conn.close()
    exit()
    return

#handle invalid opcodes
def unknown_opcode(conn):
    print "ERROR: INCORRECT OPCODE"
    return
  
#opcode associations; note that these opcodes will be returned by the serverzl;khjapoiwpe
opcodes = {'\x11': create_success,
           '\x12': general_failure,  
           '\x21': delete_success,
           '\x22': general_failure,
           '\x31': deposit_success,
           '\x32': general_failure,
           '\x41': withdraw_success,
           '\x42': general_failure,
           '\x51': balance_success,
           '\x52': general_failure,
           '\x61': end_session_success,
           '\x62': unknown_opcode
           }