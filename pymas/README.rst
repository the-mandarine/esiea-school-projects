=====
PyMAS
=====

PyMAS is a Multi-Agent System scheduler, written in Python, implementing 
the Beliefs-Desires-Intentions (BDI) software model.

It's aimed at being as light as possible to be run on any small unix
card supporting Python and to fill a very general multiagent purpose

#TODO

You can create your own modules for PyMAS in ``~/.pymas/``.
Skills module are standardized : 
This is TO DO    
    #!/usr/bin/env python
    """Description of the skill"""
    
    from math import sin
    USEFUL_FOR = ["maths", "nothing"]
    BELIEFS_KEYS = ["sinus", "stuff"]

    def is_to_execute(environment, beliefs):
        """Guesses if a module is to execute according to the current
        environment."""

        return True
    
    def execute(self):
        print("That")


System modules
==============
Several modules are already given to help the user start using PyMAS : 

Comunication
------------

* This one

* Also this one which does this, that, and even this or 
  that.


Contributors
============
Here will go the authors of PyMAS


Thanks also to
==============
The school staff who helped a lot.


