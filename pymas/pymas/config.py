"""Default config file is ~/.pymas/config 
If config args are precised they're taken."""

from persistor import Persistor, PersistorDirectory
from argparse import ArgumentParser
from os.path import expanduser, expandvars
from tempfile import mkdtemp
import sys
import logging

log = logging.getLogger(__name__)

DEFAULT_MODULES = {'belief_creator' : {}}
DEFAULT_NAME = "UnknownAgent"

class Settings(PersistorDirectory):
    """Settings contains everything needed to run an agent. It initializes a 
    really simple folder skeleton : 
    ~/.pymas/
      config
      modules/
        my_module.py
      data/
        my_persistor_directory/
          my_persistor.json
    """
    def __init__(self):
        conf = Configuration()
        PersistorDirectory.__init__(self, conf['directory'])
        self.add_persistor('config', conf)
        self.add_persistor_directory('data')
        self.add_directory('my_modules')
        self['my_modules'].add_file('__init__.py')
        self.save()


class Configuration(Persistor):
    """A configuration"""  

    def __init__(self):
        cmd_conf = CmdConfiguration().parse_args()
                
        if cmd_conf.no_write_conf:
            pymas_dir = mkdtemp("_pymas")
            cmd_conf.directory = pymas_dir
            log.info("using %s as config dir" % (pymas_dir))
        else: 
            pymas_dir = cmd_conf.directory

        if cmd_conf.debug:
            logging.basicConfig(level = logging.DEBUG)
        elif cmd_conf.info:
            logging.basicConfig(level = logging.INFO)
         
        conf_file =  pymas_dir+'/config'
        Persistor.__init__(self, conf_file)
        self.merge_config(cmd_conf)

    def merge_config(self, conf):
        """Merge a conf dictionnary in the object's internal.
        """
        loaded_conf = self.keys()
        log.debug(self)
        
        # Agent's name
        if not conf.name:
            if not 'name' in loaded_conf:
                self['name'] = DEFAULT_NAME
        else:
            self['name'] = conf.name

        # Modules to load
        cmd_line_modules = {}
        if conf.add_module is not None:
            for module_name in conf.add_module:
                cmd_line_modules[module_name] = {}

        if 'modules' not in loaded_conf:
            self['modules'] = {}

        if conf.disable_default_modules:
            self['modules'].update(cmd_line_modules)

        elif cmd_line_modules:
            self['modules'].update(DEFAULT_MODULES)
            self['modules'].update(cmd_line_modules)

        else:
            self['modules'].update(DEFAULT_MODULES)


        # User PyMAS path
        if not 'directory' in loaded_conf:
            actual_path = expanduser(expandvars(conf.directory))
            self['directory'] = actual_path
        else:
            actual_path = expanduser(expandvars(self['directory']))

        sys.path.insert(0, actual_path)

class CmdConfiguration(ArgumentParser):
    """Gets arguments from the command line"""
    def __init__ (self):
        ArgumentParser.__init__(self, 
        		description = "You can specify the agent's configuration")

        load_conf = self.add_mutually_exclusive_group()

        load_conf.add_argument('-t', '--no-write-conf', 
                action='store_true', 
                help='do not write the config file', 
                default=False)

        self.add_argument('-n', '--name', 
                help="name of the agent")

        self.add_argument('-m', '--add-module', 
                action='append', 
                help='add a defined module to load') 

        self.add_argument('--disable-default-modules', 
                action='store_true', 
                help='Disable all default modules',
                default=False)
        
        self.add_argument('-D', '--directory',
                help='directory containing all pymas config, datas, and mods',
                default='~/.pymas')

        debug = self.add_mutually_exclusive_group()

        debug.add_argument('-d', '--debug', 
                action='store_true',
                help='make the debug in DEBUG mode',
                default=False)

        debug.add_argument('-i', '--info',
                action='store_true',
                help='make the debug in INFO mode',
                default=False)

if __name__ == '__main__':
    s = Settings()
    print(s)
