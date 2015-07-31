"""Description of the module goes here"""

import re
from hashlib import md5
from time import time
from json import dumps as json_dumps

# Is the module blocking or not ?
BLOCKING = False

# Beliefs that are impacted by this module
USEFUL_FOR = ['friends']


# Commands we can send to this
RE_IP = '((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}'
RE_IP+= '(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?![\\d])'

COMMAND_RGX = '(net_analyze|net_check)::'+RE_IP+',(.*)::$'

# Net commands with believed answers (ident mostly...)
ANSWER_CMDS = ("id", "ident")
# Net commands asking a question/advice
ASK_CMDS = ("ask", "what")
# Net commands 'asking' an action
ACTION_CMDS = ("do")

def initialize(self):
    """Module initialisation"""
    log.debug("Net analyzer initialization")
    net_msg_rgx = "(.*)::(.*)::(.*)"
    data.net_msg_rgx = re.compile(net_msg_rgx)
    
    beliefs['friends'] = {}

def execute(cmd_string):
    """Check if the agent is in the beliefs
    Do what the other agent says"""
    log.debug("Analyzing net command")
    cmd, ip_from, message = re.search(COMMAND_RGX_COMP, cmd_string).groups()

    net_cmd, net_args, net_sig = re.search(data.net_msg_rgx, message).groups()
    
    agent = get_agent(ip_from)
    update_agent_time(agent)

    
    if net_cmd in ANSWER_CMDS:
        answer_cmd = update_beliefs(agent, net_cmd, net_args)

    if identified_agent(agent):
        if net_cmd in ASK_CMDS:
            answer_cmd = check_knowledges(net_cmd, net_args)
            contact_agent(ip_from, answer_cmd, message)

        if check_signature(agent, net_sig, "::".join([net_cmd, net_args])):
            if net_cmd in ACTION_CMDS:
                answer_cmd = do_something(net_cmd, net_args)

def update_beliefs(agent, cmd, args):
    """Update beliefs concerning the agent
    This function should take care to check signature for some beliefs updates
    to avoid dumb UDP spoofing leading to corrupting beliefs"""
    args_l = args.split(',')
    args_len = len(args_l)
    log.debug("updating beliefs")
    log.debug(args)
    if args_len == 2:
        #TODO tests (udp spoofing)
        log.debug("Agent " + agent['name'] + " is updating : ")
        agent[args_l[0]] = args_l[1]
        log.debug(json_dumps(agent, indent=2, sort_keys=True))
    elif args_len == 3:
        # Go with belief creator (type specification)
        a_hash = agent['ip_hash']
        args_l = args.split(',')
        attr = args_l[0]
        if attr == "address":
            address = {}
            for a_attr in args_l[1].split('/'):
                key, value = a_attr.split(':')
                address[key] = value

            if not address['host']:
                address['host'] = agent['ip_src']
            
            address_s = "/".join(["%s:%s" % (x, address[x]) for x in address.keys()])
            args_l[1] = address_s
            args = ",".join(args_l)
            
        command_queue.put_str("add_belief::friends.%s.%s::" % (a_hash, args))
        
def get_agent_by_hash(ip):
    ip_hash = md5(ip.encode()).hexdigest()
    if ip_hash in beliefs.friends.keys():
        return beliefs.friends[ip_hash]
    else:
        return False

def get_agent(ip):
    """Return an empty agent if it does not exist yet"""
    hash_agent = get_agent_by_hash(ip)
    if hash_agent:
        return hash_agent

    for friend in beliefs.friends.values():
        if friend['ip_src'] == ip:
            return friend

    agent_name = md5(ip.encode()).hexdigest()
    beliefs.friends[agent_name] = {}
    beliefs.friends[agent_name]['name'] = agent_name
    beliefs.friends[agent_name]['ip_hash'] = agent_name
    beliefs.friends[agent_name]['ip_src'] = ip

    return beliefs.friends[agent_name]

def update_agent_time(agent):
    # Last connection time
    # This is to enable some automatic flushes
    cur_time = time()
    agent['last_con'] = cur_time


def identified_agent(agent):
    """Defines if an agent has identity"""
    ip_hash = md5(agent['ip_src'].encode()).hexdigest()
    return ip_hash != agent['name']

def check_signature(agent, sig, msg):
    """Check is a signature is valid and if it's not known yet, asks friends
    and if known but unsure ask the direct person.
    If known and sure return True. Return False otherwise"""
    #TODO
    return True

def check_knowledges(net_cmd):
    """who -> .name
    you -> global_conf"""
    return False

