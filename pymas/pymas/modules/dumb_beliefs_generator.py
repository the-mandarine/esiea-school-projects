from time import sleep
from hashlib import md5

"""Description of the module goes here"""
# Is the module blocking or not ?
BLOCKING = True

PRIORITY = -2

# Beliefs that are impacted by this module
USEFUL_FOR = ['nothing']


def initialize(self):
    """Module initialisation"""
    log.debug("Dumb beliefs generator is initializing")
    data.I = 0

    for i in range(10):
        sig = md5(str(i).encode()).hexdigest()
        to_add = "add_belief::friends.agent_%s.name,agent_%s::" % (str(i), str(i))
        command_queue.put_str(to_add)
    
def execute(cmd_string):
    """This module does not care about the command string"""
    pass 

