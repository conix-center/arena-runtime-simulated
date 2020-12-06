import time

import runtimemngr.httpapp as HttpStatus

from runtimemngr.mqttmng import MqttManager
from runtimemngr.settings import Settings
from runtimemngr.runtime import Runtime
from runtimemngr.modules import ModulesControl

CFG_FILE = 'config.json'

def main():
    # load settings from json file
    Settings.load()

    # create runtime
    rt = Runtime(rt_name=Settings.s_dict['runtime']['name'], rt_max_nmodules=Settings.s_dict['runtime']['max_nmodules'], rt_apis=Settings.s_dict['runtime']['apis'], rt_dbg_topic=Settings.dbg_topic, rt_ctl_topic=Settings.ctl_topic)

    # create module ctl
    modules = ModulesControl(rt)

    # create and start mqtt client
    mqttc = MqttManager(Settings, rt, modules)
    mqttc.start(Settings.s_dict['mqtt_server']['host'], Settings.s_dict['mqtt_server']['port'], Settings.s_dict['mqtt_server']['username'], Settings.s_dict['mqtt_server']['password'])    

    # create flask app
    HttpStatus.run(rt, modules)

if __name__ == "__main__":
    main()
