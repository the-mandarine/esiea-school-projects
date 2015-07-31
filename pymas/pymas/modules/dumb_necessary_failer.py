"""This module is here to test if pyMAS is really failing (infinite loop) if
a NECESSARY module fails to execute."""
# Is the module blocking or not ?
BLOCKING = False

# Is the module necessary to the other ones
PRIORITY = -1

# Beliefs that are impacted by this module
USEFUL_FOR = ['nothing']

I = 0

class DumbFailException(Exception):
    pass

def initialize(self):
    """Module initialisation"""
    log.debug("Dumb necessary module initialization")

def execute(cmd_string):
    """This module does not care about the command string"""
    global I
    if I <= 5:
        # This will iterate 10 times before failing
        log.debug("Fail in %i iterations" % (5 - I))
        I += 1
    else:
        raise DumbFailException


    
     

