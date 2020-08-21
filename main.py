import time

import runtimemngr.httpapp as HttpStatus 

from runtimemngr.mqttmng import MqttManager
from runtimemngr.settings import Settings
from runtimemngr.runtime import Runtime
from runtimemngr.modules import ModulesControl

CFG_FILE = 'config.json'

def main():
    # read settings
    settings = Settings(CFG_FILE)

    # create runtime
    rt = Runtime(rt_name=settings.s_dict['runtime']['name'], rt_max_nmodules=settings.s_dict['runtime']['max_nmodules'], rt_apis=settings.s_dict['runtime']['apis'])
    
    # create module ctl
    modules = ModulesControl(rt)
    
    # create and start mqtt client
    mqttc = MqttManager(settings, rt, modules)
    mqttc.start(settings.s_dict['mqtt_server']['host'])    

    # create flask app
    HttpStatus.run(rt, modules)
        
if __name__ == "__main__":
    main()
    