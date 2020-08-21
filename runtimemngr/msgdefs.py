import json
import uuid
        
class Type():
    rt = 'runtime'
    mod = 'module'

class Result():
    ok = 'ok'
    err = 'error'
    
class Action():
    create = 'create'
    delete = 'delete'

class ARTSResponse(dict):
    def __init__(self, r_uuid, result, details):
        dict.__init__(self, object_id=str(r_uuid), type='arts_resp', data={ 'result': result, 'details': details })

class ARTSRequest(dict):
    def __init__(self, r_uuid, action, type, obj={}): # obj can have uuid already
        rdata = { 'type': type }
        #for key, value in obj.items():
        #    rdata[key] = str(value)
        rdata.update(obj)
        dict.__init__(self, object_id=str(r_uuid), action=action, type='arts_req', data=rdata)
        