"""Description of the module goes here"""

# Is the module blocking or not ?
BLOCKING = False

# Beliefs that are impacted by this module
USEFUL_FOR = ['nothing']

# Commands we can send to this
COMMAND_WORDS = ['add_belief']

PRIORITY = 3

def initialize(self):
    """Module initialization"""
    log.debug("Belief generator initialization")

def execute(cmd_string):
    """Execute the command string"""
    if cmd_string:
        cmd_l = cmd_string.split('::')
        args = cmd_l[1].split(',')
        bel_key = args[0]
        bel_value = args[1]           
        create_dict(beliefs, bel_key, bel_value)
        log.debug('%s <- %s' % (bel_key, bel_value)) 
		 
def create_dict(container, key_string, value):
	""" Create dictionnary in container"""
	key_l=key_string.split(".")
	if len(key_l) == 1:
		container[key_string]=value
	else:
		if key_l[0] not in container:
			container[key_l[0]]= {}
		
		create_dict(container[key_l[0]], '.'.join(key_l[1:]),value)
	

