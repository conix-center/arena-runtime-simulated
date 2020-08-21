
import os
import sys
import shlex
import subprocess
import threading
import time
import json
import signal
import atexit    
# conditional import for runnig standalone
try:
    import runtimemngr.settings as settings
except ImportError:
    import settings

class FileType():   
    WA = 'WASM'
    PY = 'PY'
    
class ModuleLaucher():

    def __init__(self):
        self.lock = threading.Lock()
        self.proclist = {}
        self.allDone = False
        atexit.register(self.killAll)

    def _run_thread(self, cmd, env, muuid):
        proc = subprocess.Popen(cmd, env=env, shell=False,  preexec_fn=os.setsid)
        self.lock.acquire()
        self.proclist[muuid] = proc
        self.lock.release()
        while (1) :
            ret = proc.poll()
            if (ret):
                # process terminated
                self.lock.acquire()
                try:
                    self.proclist.pop(muuid)
                except:
                    print("Could not remove process from process list.")
                self.lock.release()
                return

    def kill(self, muuid):
        try:
            self.lock.acquire()
            proc = self.proclist[muuid]
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            self.lock.release()
        except:
            print("Could not find module", muuid)

    def killAll(self):
        self.lock.acquire()
        for muuid, proc in self.proclist.items():
            print("Killing", muuid)
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except:
                print("Could not kill module", muuid)
            self.allDone = True
        self.lock.release()

    def isAllDone(self):
        self.lock.acquire()
        r = self.allDone
        self.lock.release()
        return r
        
    def run(self, module, rt_dbg_topic, rt_ctl_topic, done_msg):
        cmd = []
        
        if module.uuid in self.proclist.keys():
            raise Exception("Module already running (duplicate uuid)") 
            
        if (module.filetype == FileType.PY):
            cmd.append(settings.s_dict['runtime']['py_launcher_path']) 
        else:
            raise Exception("We only support python files") 
        #elif (module.filetype == FileType.WA):
        #    cmd.append(settings.s_dict['runtime']['wasm_launcher_path'])

        stdin_topic = rt_dbg_topic+'/stdin/'+module.uuid
        stdout_topic = rt_dbg_topic+'/stdout/'+module.uuid

        # start our variables with __ so they do not collide with module's variables
        env = { 
                '__mqtt_srv' : shlex.quote(settings.s_dict['mqtt_server']['host']), 
                '__name': shlex.quote(module.name),
                '__store_url': shlex.quote(settings.s_dict['store_url']),
                '__filename': shlex.quote(module.filename), 
                '__fid': shlex.quote(module.fileid), 
                '__pipe_stdin_stdout': 'True', 
                '__sub_topic': shlex.quote(stdin_topic),
                '__pub_topic': shlex.quote(stdout_topic),
                '__args': shlex.quote(module.args),
                '__env': shlex.quote(module.env),
                '__done_topic': shlex.quote(rt_ctl_topic+"/"+module.uuid),
                '__done_msg': shlex.quote(done_msg)}

        if (module.env.find(' ') != -1): 
            for vstr in module.env.split(" "):
                v = vstr.split("=")
                env[v[0]]=v[1]
        elif (module.env.find('=') != -1):
            module.env = vstr.split("=")
            env[v[0]]=v[1]   
            
        print('env=',env)
        print('cmd=',cmd)
        t = threading.Thread(target=self._run_thread, args=(cmd, env, module.uuid))
        t.start()
        
# run standalone (for simple testing)
def main():
    m = ModuleLaucher()
        
    settings.load()

    class Module(object): pass
    mod = Module()
    mod.uuid='18881342-4111-488d-9301-064ad9b4d39a'
    mod.name='npereira/pytest'
    mod.filename='test.py'
    mod.fileid='fid'
    mod.filetype='PY'
    mod.args='test'
    mod.env='ENV_VAR1=1 ENV_VAR2=2'

    try:
        m.run(mod, 'realm/proc/debug', 'realm/proc/stdout/', '')
    except Exception as err:
        print(err)
        
    time.sleep(5)
    
    mod1 = Module()
    mod1.uuid='18881342-4111-488d-9301-064ad9b4d39b'
    mod1.name='npereira/pytest'
    mod1.filename='test.py'
    mod1.fileid='fid'
    mod1.filetype='PY'
    mod1.args='test'
    mod1.env='ENV_VAR1=1 ENV_VAR2=2'

    try:
        m.run(mod1, 'realm/proc/debug', 'realm/proc/stdout/', '')
    except Exception as err:
        print(err)

    time.sleep(5)
    
    print('killing: ', mod.uuid)
    m.kill(mod.uuid)
        
    while m.isAllDone()==False:
        time.sleep(1)

if __name__ == "__main__":
    
    main()