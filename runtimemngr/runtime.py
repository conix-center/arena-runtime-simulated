"""
*TL;DR
Runtime class; Store information about the runtime
"""

from runtimemngr.msgdefs import ARTSRequest, Action, Type
import json
import uuid

class Runtime(dict):
    type = Type.rt
    def __init__(self, rt_name, rt_uuid=str(uuid.uuid4()), rt_max_nmodules=100, rt_apis=['wasi:snapshot_preview1', 'python:python3'], rt_dbg_topic='realm/proc/debug', rt_ctl_topic='realm/proc/control'):
        dict.__init__(self, uuid=rt_uuid, name=rt_name, max_nmodules=rt_max_nmodules, apis=rt_apis, dbg_topic=rt_dbg_topic, ctl_topic=rt_ctl_topic)

    @property
    def uuid(self):    
        return self['uuid']

    @uuid.setter
    def uuid(self, rt_uuid):    
        self['uuid'] = str(rt_uuid)
    
    @property
    def name(self):    
        return self['name']

    @name.setter
    def name(self, rt_name):    
        self['name'] = rt_name

    @property
    def max_nmodules(self):    
        return self['max_nmodules']

    @max_nmodules.setter
    def max_nmodules(self, rt_max_nmodules):    
        self['max_nmodules'] = rt_max_nmodules

    @property
    def apis(self):    
        return self['apis']

    @apis.setter
    def apis(self, rt_apis):    
        self['apis'] = rt_apis

    @property
    def dbg_topic(self):    
        return self['dbg_topic']

    @dbg_topic.setter
    def dbg_topic(self, dbg_topic):    
        self['dbg_topic'] = dbg_topic

    @property
    def ctl_topic(self):    
        return self['ctl_topic']

    @ctl_topic.setter
    def ctl_topic(self, ctl_topic):    
        self['ctl_topic'] = ctl_topic

    @property
    def reg_topic(self):    
        return self['reg_topic']

    @reg_topic.setter
    def reg_topic(self, reg_topic):    
        self['reg_topic'] = reg_topic
        
        
class RuntimeView():
                    
    # utility function to return a register message
    def json_reg(self, reg_uuid, runtime):
        return json.dumps(ARTSRequest(reg_uuid, Action.create, runtime.type, runtime))

    # utility function to return a unregister (delete) message
    def json_unreg(self, reg_uuid, runtime):
        req = ARTSRequest(reg_uuid, Action.delete, runtime.type, runtime)
        print(req)
        return json.dumps(req)

    # utility function to return a request
    def json_req(self, runtime, action):
        return json.dumps(ARTSRequest(uuid.uuid4(), action, runtime.type, runtime))
