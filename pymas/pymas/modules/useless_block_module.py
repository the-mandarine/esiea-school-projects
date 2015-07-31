"""Description of the module goes here"""
# Is the module blocking or not ?
BLOCKING = True

# Beliefs that are impacted by this module
USEFUL_FOR = ['nothing']

# Commands we can send to this
COMMAND_WORDS = ['print']

# Datas in the module 
DATAS = object()

# Only the concerned beliefs are sent
# All desires are sent
# To create de new belief, you must generate a desire (see belief_creator.py)
def initialize(self):
    """Module initialisation"""
    log.debug("Useless blocking module initialization")

def execute(cmd_string):
    """Execute the command string"""
    cmd_list = cmd_string.split('::')
     
    print("Useless blocking " + cmd_list[1])

