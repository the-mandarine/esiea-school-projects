"""Handle all BDI interactions
These objects are all serializable."""

class BeliefHandler(dict):
    """Clearly a selective accessor to beliefs"""
    def __init__(self, base_dict, module = None):
        #Limiting the access to some values
        if module:
            self.access = module.USEFUL_FOR

    def add(self, key, value):
        self[key] = value

    def remove(self, key):
        del self[key]

    def get_by_key(self, key):
        #TODO limit
        return get_in_dict(self, key)

def get_in_dict(container, key):
    key_l = key.split('.')
    if len(key_l) == 1:
        return container[key_l[0]]
    else:
        return get_in_dict(container[key_l[0]], '.'.join(key_l[1:])) 
