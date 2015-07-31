"""The scheduler is the main component. It loads, unloads, send and receive 
modules from and to other agents.
See the see/ask protocol"""

from threading import Thread, RLock
from time import sleep
from bdi import BeliefHandler, DesireHandler
from modules import BlockingLauncher, NonBlockingLauncher
from modules import Command
from imp import reload as module_reload
from queue import Queue
import sys
import logging

log = logging.getLogger(__name__)

AUTHORIZED_MODULE_COMMANDS = [
    'load_module',
    'unload_module',
    'stop',
    ]

GENERAL_BH = BeliefHandler({})
GENERAL_DH = DesireHandler({})

class Agent(Thread):
    """Main component. Loads and unloads modules calling them according to
    beliefs and desires to generate intentions"""
    
    def __init__(self, settings):
        Thread.__init__(self)
        self.settings = settings
        self.config = settings['config']
        self.name = self.config['name']
        self.terminated = False

        self.blocking_modules = []
        self.non_blocking_modules = []
        self.command_queue = GeneralCommandQueue(self)
        self.command_queue.start()

        self.base_beliefs = {}
        self.base_desires = {}

        self.load_config_modules(self.config)

    def run(self):
        while not self.terminated:
            for module in self.non_blocking_modules:    
                if module.priority < 0:
                    module.execute(necessary = True)
                else:
                    module.execute()
                    sleep(0.5)

    def stop(self):
        """Unload every module and stop the scheduler thread"""
        self.terminated = True


        for module in self.blocking_modules:
            module.stop()

        for module in self.non_blocking_modules:
            module.stop()
        
        self.command_queue.put_str("event::agent_stop::")
        sleep(0.5)
        self.command_queue.stop()
        log.info("* Agent stopped")

    def load_module(self, module_name, module_conf = None, userspace = True):
        """Loads a module inside the agent"""
        if userspace:
            to_load = "my_modules." + module_name
        else:
            to_load = "modules." + module_name

        log.info("Loading from : %s" % (to_load))

        try:
            __import__(to_load)
            module = sys.modules[to_load]
            module_reload(module)

            if not module_conf:
                if hasattr(module, "DEFAULT_CONF"):
                    module_conf = module.DEFAULT_CONF
                    self.config['modules'][module_name] = module_conf
                    self.config.save()

            if module.BLOCKING:
                # Start in a new thread
                launcher = BlockingLauncher(module, module_conf, self.config)
                self.blocking_modules.append(launcher)
                self.blocking_modules.sort()

            else:
                # Or not
                launcher = NonBlockingLauncher(module, module_conf, self.config)
                self.non_blocking_modules.append(launcher)
                self.non_blocking_modules.sort()

            
            # Give it a command queue
            launcher.attach_command_queue(self.command_queue)
            self.command_queue.modules.append(launcher)
            self.command_queue.modules.sort()

            # TODO delete this 
            # TODO initialization
            if 'initialize' in module.__dict__.keys():
                bel_handler, des_handler = self.generate_handlers(module)
                launcher.initialize(bel_handler, des_handler)
            else:
                log.error(module_name, "The `initialize` function misses")
                return False
            
            #self.command_queue.nb_modules += 1

            # Start the launcher
            launcher.start()
            belief_cmd = "add_belief::modules.%s.loaded,true,b::" % module_name
            self.command_queue.put_str(belief_cmd)
            return True

        except ImportError:
            if userspace:
                return self.load_module(module_name, module_conf, False)
            else:
                log.error("Module loading fail : %s" % (module_name))
                return False
    
    def unload_module(self, module_name):
        to_unload = "modules."+module_name
        for module in self.blocking_modules:
            if module.name == to_unload:
                module.stop()
                self.blocking_modules.remove(module)

        for module in self.non_blocking_modules:
            if module.name == to_unload:
                module.stop()
                self.non_blocking_modules.remove(module)
        
        for module in self.command_queue.modules:
            if module.name == to_unload:
                self.command_queue.modules.remove(module)

        self.config['modules'].pop(module_name)
        belief_cmd = "add_belief::%s_loaded,false,b::" % module_name
        self.command_queue.put_str(belief_cmd)

    def generate_handlers(self, module):
        #TODO
        belief_h = GENERAL_BH
        desire_h = GENERAL_DH
        return belief_h, desire_h


    def load_config_modules(self, conf):
        """Loads blocking modules and non-blocking ones in separate lists"""
        for module_to_load in conf['modules'].keys():
            log.info("Loading : %s" % module_to_load)
            mod_conf = conf['modules'][module_to_load]
            
            if self.load_module(module_to_load, mod_conf):
                log.info("Loaded : %s" % module_to_load)

    def treat_cmd(self, cmd_s):
        """Treats a raw Agent command (starts with __agent_)
        Here the command will be given without the __agent_"""
        cmd_l = cmd_s.split('::')
        cmd_c = cmd_l[0]
        cmd_a = cmd_l[1].split(',')

        if cmd_c in AUTHORIZED_MODULE_COMMANDS:
            getattr(self, cmd_c)(*cmd_a)

class GeneralCommandQueue(Thread):
    """Wrapper for the queue class"""
    def __init__(self, agent):
        Thread.__init__(self)
        self.queue_in = Queue()
        self.modules = []
        self.lock = RLock()
        self.agent = agent
        self.terminated = False

    def stop(self):
        self.terminated = True
        log.debug("Command queue stopped")

    def run(self):
        while not self.terminated:
            if not self.queue_in.empty():
                command = self.queue_in.get()
                log.debug("new command:<%s>" % (command.string))

                for mod in self.modules:
                    mod.command_queue.put_local(command)
            else:
                sleep(1)
                    

    def put(self, cmd):
        self.queue_in.put(cmd)

        # Check for raw agent command
        # TODO tmbabw
        if cmd.string.startswith("__agent_"):
            self.agent.treat_cmd(cmd.string.split("__agent_")[1])
        
    def put_str(self, cmd_str):
        cmd = Command(cmd_str)
        self.put(cmd)

