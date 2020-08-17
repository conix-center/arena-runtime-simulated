
import os
import sys
import shlex
import subprocess
import threading

import asyncio
#import clauncher.settings as settings
import time

import json

class FileType():   
    WA = 'WASM'
    PY = 'PY'

class Foo(object):
    pass   
            
settings =Foo()
    
class ModuleLaucher():

    def _run_thread(self, cmd, env):
        subprocess.run(cmd, env=env)

    def run_command(cmd, env):
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline,''):
            print(line.rstrip())
        # while True:
        #     output = process.stdout.readline()
        #     if output == '' and process.poll() is not None:
        #         break
        #     if output:
        #         print output.rstrip()
        # rc = process.poll()
        # return rc
                     
    def run(self, module, dbg_topic, done_topic, done_msg):
        cmd = []
        
        if (module.filetype == FileType.PY):
            cmd.append(settings.s_dict['runtime']['py_launcher_path']) 
        elif (module.filetype == FileType.WA):
            cmd.append(settings.s_dict['runtime']['wasm_launcher_path'])

        stdin_topic = dbg_topic+'/stdin/'+module.uuid
        stdout_topic = dbg_topic+'/stdout/'+module.uuid

        env = { 
                'mqtt_srv' : shlex.quote(settings.s_dict['mqtt_server']['host']), 
                'filename': shlex.quote(module.filename), 
                'fid': shlex.quote(module.fileid), 
                'pipe_stdin_stdout': 'True', 
                'sub_topic': shlex.quote(stdin_topic),
                'pub_topic': shlex.quote(stdout_topic),
                'args': shlex.quote(module.args),
                'done_topic': shlex.quote(done_topic),
                'done_msg': shlex.quote(done_msg)}
        
        print('env=',env)
        print('cmd=',cmd)
        #t = threading.Thread(target=self._run_thread, args=(cmd, env))
        #t.start()
        self.run_command(cmd, env)

def main():
    with open('config.json') as json_data_file:
        settings.s_dict = json.load(json_data_file)

    m = ModuleLaucher()
    mod = Foo()
    mod.uuid='18881342-4111-488d-9301-064ad9b4d39b'
    mod.name='mod1'
    mod.filename='test.py'
    mod.fileid='fid'
    mod.filetype='PY'
    mod.args='test'

    m.run(mod, 'realm/proc/stdin/'+mod.uuid, 'realm/proc/stdout/'+mod.uuid, '')
    
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()