"""Handle all BDI interactions
These objects are all serializable."""


class Belief(object):
    """What the agent 'think' of the environnement"""
    pass

class Desire(object):
    """What the whole network want to do"""
    pass

class Skill(Belief):
    """Local belief concerning an agent capacity"""
    pass

class SharedData(Belief):
    """Shared belief amond the whole network"""
    pass


class BeliefHandler(dict):
    """Clearly a selective accessor to beliefs"""

    def __init__(self, base_dict, module = None):
        #Limiting the access to some values
        #TODO
        if module:
            self.access = module.USEFUL_FOR

    def __getattr__(self, attr):
        return self.get(attr, None)

    def add(self, key, value):
        self[key] = value

    def remove(self, key):
        del self[key]

    def get_by_key(self, key):
        return get_in_dict(self, key)

def get_in_dict(container, key):
    #print(container, key)
    if type(container) in (BeliefHandler, dict):
        key_l = key.split('.')
        if len(key_l) == 1:
            return container[key_l[0]]

        else:
            return get_in_dict(container[key_l[0]], '.'.join(key_l[1:])) 
    else:
        return None

class DesireHandler(dict):
    """An accessor to desires. Should rarely be selective"""
    def __init__(self, base_dict, module = None):
        #TODO
        pass

def beliefs_from_keys(keys = [], *args):
    """Return a dict of asked named beliefs"""
    beliefs = {}

    return beliefs

