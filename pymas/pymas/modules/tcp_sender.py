"""Description of the module goes here"""

from socket import socket, AF_INET, SOCK_STREAM

# Is the module blocking or not ?
BLOCKING = False

# Beliefs that are impacted by this module
USEFUL_FOR = ['net']

# Commands we can send to this
COMMAND_WORDS = ['tcp_send']

def initialize(self):
    """Module initialisation"""
    log.debug("TCP Sender module initialization")

def execute(cmd_string):
    """Execute the command string : udp_send::ip,port,message::opts"""
    cmd_list = cmd_string.split('::')
    cmd_args = '::'.join(cmd_list[1:-1]).split(',')
    dest_host = cmd_args[0]
    dest_port = int(cmd_args[1])
    message = cmd_args[2].encode()
    print("TENTATIVE D'ENVOI TCP !!!!11")
        
    data.sock = socket(AF_INET, SOCK_STREAM)
    try:
        data.sock.connect( (dest_host, dest_port) )
        data.sock.send(message)
        data.sock.close()
    except:
        pass

