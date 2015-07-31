from time import sleep

"""Description of the module goes here"""
# Is the module blocking or not ?
BLOCKING = False

PRIORITY = -1

# Beliefs that are impacted by this module
USEFUL_FOR = ['nothing']

def initialize(self):
    """Module initialisation"""
    log.debug("Dumb necessary module initialization")
    data.i = 0

def execute(cmd_string):
    """This module does not care about the command string"""
    if data.i == 0: 
        #add_to_queue = "tcp_send::localhost,7878,message_%s::" % (data.i)
        #add_to_queue = "friend::udp,localhost,8989::"
        
        add_to_queue = "say::TRUC::"
        command_queue.put_str(add_to_queue)
        
        add_to_queue = "say::TRUC::"
        command_queue.put_str(add_to_queue)
        data.i += 1
        

