"""Global modules here such as : 
"""

from threading import Thread, Event
from queue import Queue
from time import sleep
import logging
import re
import sys

log = logging.getLogger(__name__)

class ModuleLauncher(object):
    
    def __init__(self, module, mod_conf, global_conf):
        self.module = module
        self.name = module.__name__
        self.module.log = logging.getLogger(self.name)
        self.module.conf = mod_conf
        self.module.global_conf = global_conf
        self.module.data = DataHandler()
        self.command_queue = LocalCommandQueue()
        self.module.command_queue = self.command_queue
        self.priority = 0
        self.terminated = False

    def attach_command_queue(self, queue):
        self.command_queue.attach(queue)

    def module_concerned(self, command):
        """Defines if a module is concerned about a command"""
        concerned = False
        if command:
            command_word = command.string.split('::')[0]

            if "COMMAND_WORDS" in self.module.__dict__:
                if command_word in self.module.COMMAND_WORDS:
                    concerned = True

            if "COMMAND_RGX_COMP" in self.module.__dict__:
                if re.search(self.module.COMMAND_RGX_COMP, command.string):
                    concerned = True

        return concerned

    def initialize(self, bel_h, des_h):
        self.module.beliefs = bel_h
        self.module.desires = des_h
        
        if "COMMAND_RGX" in self.module.__dict__:
            self.module.COMMAND_RGX_COMP = re.compile(\
                self.module.COMMAND_RGX)

        if "PRIORITY" in self.module.__dict__:
            self.priority = self.module.PRIORITY


    def __lt__(self, module):
        return self.priority < module.priority

    def __le__(self, module):
        return self.priority <= module.priority

    def __gt__(self, module):
        return self.priority > module.priority

    def __ge__(self, module):
        return self.priority >= module.priority

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def stop(self):
        self.terminated = True
        if hasattr(self.module, "stop"):
            self.module.stop()


class BlockingLauncher(Thread, ModuleLauncher):
    
    def __init__(self, module, conf, glob_conf):
        Thread.__init__(self)
        self.daemon = True
        ModuleLauncher.__init__(self, module, conf, glob_conf)
    
    def run(self):
        self.module.initialize(self)
        while not self.terminated:
            command = self.command_queue.get(source = self)
            if command:
                if self.module_concerned(command):
                    self.module.execute(command.string)
            
            sleep(0.5)



class NonBlockingLauncher(ModuleLauncher):    
    def start(self):
        self.module.initialize(self)

    def execute(self, necessary = False):
        command = self.command_queue.get(source = self)
        if necessary:
            self.terminated = False
            while not self.terminated:
                try:
                    self.module.execute(command.string)

                    self.terminated = True
                except:
                    log.info("Necessary module failed : " + self.name)
                    log.info("This can result in infinite looping.")
                    log.debug(sys.exc_info())
                    sleep(0.5)

        else:   
            if self.module_concerned(command):
                self.module.execute(command.string)


class LocalCommandQueue(object):
    def __init__(self):
        self.queue = Queue()
        self.queue_out = None
    
    def attach(self, queue):
        self.queue_out = queue

    def get(self, source = None):
        if not self.queue.empty():
            ret = self.queue.get()
        else:
            ret = Command(None)

        return ret

    def put_local(self, obj):
        self.queue.put(obj)

    def put(self, obj):
        self.queue_out.put(obj)
    
    def put_str(self, obj):
        self.queue_out.put_str(obj)


class Command(object):
    """Defines a command readable only one time by the same module"""
    def __init__(self, cmd_str):
        self.string = cmd_str

    def __unicode__(self):
        return self.string

    def __bool__(self):
        return self.string is not None


class DataHandler(object):
    pass

