"""Description of the module goes here"""

import sys

# Is the module blocking or not ?
BLOCKING = False

# Beliefs that are impacted by this module
USEFUL_FOR = ['nothing']

# Commands we can send to this
#COMMAND_WORDS = ['print', 'echo', 'say']

# Commands we can send
COMMAND_RGX = "^(print|echo|say)::.*?"

def initialize(self):
    """Module initialisation"""
    log.debug("Useless module initialization")

def execute(cmd_string):
    """Execute the command string"""

    cmd_list = cmd_string.split('::')
