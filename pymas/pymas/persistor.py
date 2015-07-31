"""Handles persistent datas : logs, expression libraries, auth
Only text is handled here.
Data are stocked into a json form."""

from json import dumps as json_dumps, loads as json_loads
from os.path import exists, expanduser, expandvars, dirname, isdir
from os import makedirs
from tempfile import mkstemp

class Persistor(dict):
    """A huge dict to handle persistent datas like a shelf"""
    def __init__(self, name = None, data = {}):
        dict.__init__(self)

        self.new = False
        if name is None:
            file_mode, self.file_name = mkstemp('.json')
        else:
            self.file_name = expanduser(expandvars(name+'.json'))
        
        self.load()
        self.update(data)

    def __str__(self):
        json_string = json_dumps(self, sort_keys = True, indent = 2)
        return json_string

    def load(self):
        """Loads the specified file into the dict"""
        self.clear()
        if exists(self.file_name):
            with open(self.file_name, 'r') as file_descr:
                json_string = file_descr.read()
            try:
                dict_to_load = json_loads(json_string)
            except ValueError:
                dict_to_load = {}
                self.new = True
        else:
            dict_to_load = {}
            self.new = True

        for key in dict_to_load.keys():
            self[key] = dict_to_load[key]

    def save(self, no_fail = False):
        """Saves the dict into the persistor file."""
        json_string = str(self)
        try:
            with open(self.file_name, 'w') as file_descr:
                file_descr.write(json_string)
        except IOError as err:
            if no_fail:
                print("I/O error: {0}".format(err))
                exit(4)
            else:
                # Probably the folder isn't created
                makedirs(dirname(self.file_name))
                self.new = True
                self.save(no_fail = True)

class PersistorDirectory(dict):
    """Dict to handle datas in files in a directory"""
    def __init__(self, path):
        absolute_path = expanduser(expandvars(path))
        if not isdir(absolute_path):
            makedirs(absolute_path)

        self.path = absolute_path
    
    def add_persistor(self, name, persistor = None):
        self[name] = Persistor(self.path+'/'+name)
        if persistor is not None:
            self[name].update(persistor)
        # Any operation to do on newly attached persistor ?
        
    def add_persistor_directory(self, name, persistor_dir = None):
        self[name] = PersistorDirectory(self.path+'/'+name)
        if persistor_dir is not None:
            self[name].update(persistor_dir)
        # Any operation to do on newly attached persistor directory ?

    def add_directory(self, path):
        self.add_persistor_directory(path)

    def add_file(self, path):
        file_path = self.path+'/'+path
        descriptor = open(file_path, 'w')
        descriptor.close()

    def save(self):
        """Write on files"""
        for key in self.keys():
            if type(self[key]) in (Persistor, PersistorDirectory):
                self[key].save()
                
            else:
                print(type(self[key]), self[key])
    
if __name__ == '__main__':
    """Test function"""
    p_dir = PersistorDirectory("test_per_dir")
    p_dir.add_persistor("per1")
    p_dir['per1']['key1'] = {'subkey1':'subvalue1'}
    p_dir['per1']['key2'] = ['value2', 'value3']
    p_dir.add_persistor_directory("sub_per_dir")
    p_dir['sub_per_dir'].add_persistor("per2")
    p_dir['sub_per_dir']['per2']['key3'] = "value4"
    p_dir.save()
    print(p_dir)

