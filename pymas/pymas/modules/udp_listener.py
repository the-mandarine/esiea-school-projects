"""Description of the module goes here"""

from socket import socket, AF_INET, SOCK_DGRAM, error as sock_err

# Is the module blocking or not ?
BLOCKING = False

# Beliefs that are impacted by this module
USEFUL_FOR = ['nothing']

PRIORITY = -5

COMMAND_RGX = ".*"

DEFAULT_CONF = {
    "host": "",
    "port":7878
}

def initialize(self):
    """Module initialisation"""
    data.udp_listener = socket(AF_INET, SOCK_DGRAM)
    data.udp_listener.bind( (conf['host'], conf['port']) )
    data.udp_listener.setblocking(0)

def execute(cmd_string):
    """Execute the command string"""
    try:
        udp_data, udp_agent = data.udp_listener.recvfrom(1024)
    except sock_err:
        return

    if udp_data:
        log.debug(udp_data)
        command = "net_analyze::%s,%s::" % (udp_agent[0], udp_data.decode())
        command_queue.put_str(command)

    return True

