"""Send UDP message to a specific destination"""

from socket import socket, AF_INET, SOCK_DGRAM
BLOCKING = False
COMMAND_WORDS = ['udp_send']

def initialize(self):
    """Module initialisation"""
    log.debug("UDP Sender module initialization")

def execute(cmd_string):
    """Execute the command string : udp_send::ip,port,message::opts"""
    cmd_list = cmd_string.split('::')
    cmd_args = '::'.join(cmd_list[1:-1]).split(',')
    dest_host = cmd_args[0]
    dest_port = int(cmd_args[1])
    message = ','.join(cmd_args[2:]).encode()

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.sendto(message, (dest_host, dest_port))

