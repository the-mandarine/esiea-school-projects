"""Description of the module goes here"""

import sys

BLOCKING = False

USEFUL_FOR = ['nothing']

PRIOTIRY = 2

COMMAND_WORDS = ['id_to', 'new_friend', 'friend', '__agent_load_module', 
'__agent_unload_module']

def initialize(launcher):
    """Module initialisation"""
    update_net_list()

def execute(cmd_string):
    """Execute the command string"""
    cmd_list = cmd_string.split('::')
    if cmd_list[0].startswith('__agent_'):
        update_net_list()
    else:
        for net_s in get_net_strings():
            command_queue.put_str("net_send::%s,id::address,%s,l::" % (cmd_list[1], net_s))

def update_net_list():
    data.net_modules = {}
    for module in global_conf['modules'].keys():
        module_l = module.split('_')
        if module_l[-1] == 'listener':
            protocol = '_'.join(module_l[:-1])
            data.net_modules[protocol] = global_conf['modules'][module]

    # data.net_modules now contains protocols of listeners
    return data.net_modules

def get_net_strings():
    net_strings = []
    for net_m in data.net_modules.keys():
        net_str = "prot:" + net_m + '/'
        for attr in data.net_modules[net_m].keys():
            net_str += "%s:%s/" % (attr, data.net_modules[net_m][attr])

        real_net_str = net_str[:-1]
        net_strings.append(real_net_str)

    return net_strings

