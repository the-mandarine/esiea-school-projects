"""Description of the module goes here"""

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET
from socket import SO_REUSEADDR, error as sock_err
from queue import Queue
from threading import Thread
# Is the module blocking or not ?
BLOCKING = True

# Beliefs that are impacted by this module
USEFUL_FOR = ['nothing']

PRIORITY = -5

COMMAND_RGX = ".*"

DEFAULT_CONF = {
    "host": "",
    "port":7878
}

def initialize(agent):
    """Module initialisation"""
    data.tcp_listener = socket(AF_INET, SOCK_STREAM)
    data.tcp_listener.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    data.tcp_listener.bind( (conf['host'], conf['port']) )
    data.tcp_listener.listen(5)
    data.connections = {}
    data.terminated = False
    log.debug("initialized")

def stop(): 
    data.terminated = True

    for handler in data.connections.keys():
        data.connections[handler].close()

    data.tcp_listener.close()


def execute(cmd_string):
    """Execute the command string"""
    log.debug("waiting for connection")
    if not data.terminated:
        try:
            conn, addr = data.tcp_listener.accept()
            print("TCP : CONNEXION")
            handler = TCPSocketHandler(conn, addr)
            data.connections[addr] = handler
            handler.start()
        except sock_err:
            pass
        # Add the corresponding belief
        #TODO

    return True

class TCPSocketHandler(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.terminated = False
    
    def close(self):
        self.conn.close()

    def run(self):
        while not self.terminated:
            try:
                received = self.conn.recv(1024)
            except sock_err:
                print("Disconnected")
                self.terminated = True

            if not received:
                self.terminated = True
            else:
                received_string = received.decode()
                #received_string = received
                cmd = "net_analyze::%s,%s::" % (self.addr[0], received_string)
                command_queue.put_str(cmd)

