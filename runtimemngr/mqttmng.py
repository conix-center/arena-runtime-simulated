
import paho.mqtt.client as mqtt
import threading
import json 
import uuid
import time

from runtimemngr.runtime import RuntimeView
from runtimemngr.msgdefs import Action, Result, ARTSResponse


class MqttManager(mqtt.Client):

    def __init__(self, settings, rt, modules):
        super(MqttManager, self).__init__(str(rt.uuid))
        self.runtime = rt 
        self.reg_attempts = 0
        
        # save settings
        self.settings = settings
        self.reg_topic = settings.reg_topic
        self.ctl_topic = settings.ctl_topic
        self.dbg_topic = settings.dbg_topic

        self.modules = modules
        
    def wait_timeout(self, tevent, stime, callback):
        print('****waiting')
        time.sleep(stime)
        if tevent.isSet() == False:
            callback()
    
    # TODO: do not start a new thread for each timeout
    def set_timeout(self, timeout, callback):
        timeout_event = threading.Event()
        t = threading.Thread(target=self.wait_timeout, args=(timeout_event, timeout, callback))
        t.start()
        return timeout_event

    def register_rt(self):
        # this will use the current runtime uuid as the object id
        self.reg_uuid = uuid.uuid4()
        reg_msg = RuntimeView().json_reg(self.reg_uuid, self.runtime)
        print('Registering: ', reg_msg)
        self.publish(self.reg_topic, reg_msg)
        self.reg_attempts += 1
        if (self.settings.s_dict['runtime']['reg_attempts'] == 0 or self.settings.s_dict['runtime']['reg_attempts'] > self.reg_attempts):        
            self.reg_done = self.set_timeout(self.settings.s_dict['runtime']['reg_timeout_seconds'], self.register_rt)
    
    def on_connect(self, mqttc, obj, flags, rc):
        print('registering runtime')         
        try: 
            self.register_rt()
        except Exception as err:
            print(err)
    
    def on_message(self, mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        
        str_payload = str(msg.payload.decode("utf-8","ignore"))
        
        if (len(str_payload) == 0): # ignore 0-len payloads
            return
        
        # reg_topic msg 
        if (msg.topic == self.reg_topic):
            try:
                reg_msg = json.loads(str_payload) # convert json payload to a python string, then to dictionary
            except Exception as err:
                print('Error parsing message to reg:', err)
                return
             
            if (reg_msg['type'] != 'arts_resp'): # silently return if type is not arts_resp!
                return
            
            # we are only interested in reg message confirming our registration 
            if reg_msg['object_id'] != str(self.reg_uuid):
                return

            # check if result was ok
            if reg_msg['data']['result'] != Result.ok:
                print('Register failed; Retrying') # we do not set the reg timeout event, so will try again
                return
            
            # cancel timeout; will not retry reg again
            self.reg_done.set()
            
            # unsubscribe from reg topic and subscribe to ctl/runtime_uuid
            self.unsubscribe(self.reg_topic)
            self.ctl_topic += '/' + str(self.runtime.uuid)
            self.subscribe(self.ctl_topic)
            
        # ctl_topic msg 
        if (msg.topic == self.ctl_topic):
            try:
                ctl_msg = json.loads(str_payload) # convert json payload to a python string, then to dictionary
            except Exception as err:
                print('Error parsing message to ctl:', err)
                return
            
            #print(ctl_msg)
            
            if (ctl_msg['type'] == 'arts_req'):
                # module create
                # example msg:
                #   { "object_id": "f9f33440-4cb7-47a2-bcd2-0ddcac362dae", "action": "create", "type": "arts_req", "data": { "type": "module", "name": "npereira/pytest", "filename": "test.py", "fileid": "na", "filetype": "PY", "args": "", "env": "", "channels": "" }
                if (ctl_msg['action'] == 'create' and ctl_msg['data']['type'] == 'module'):
                    mod_data = ctl_msg['data']
                    #print("mod_data: ", mod_data)
                          
                    try:            
                        ## missing mandatory fields will cause an exception
                        mod = self.modules.create(mod_data['uuid'], mod_data['name'], mod_data['filename'], mod_data.get('fileid', ''),mod_data['filetype'],mod_data.get('args', ''), mod_data.get('env', ''))
                    except Exception as err:
                        print('Error creating new module:', err)                        
                        resp = ARTSResponse(ctl_msg['object_id'],Result.err, 'Module could not be created; {1}'.format(err))
                        self.publish(self.ctl_topic, json.dumps(resp))
                        return                      

                    print('Sending Confirmation!')
                    resp = ARTSResponse(ctl_msg['object_id'],Result.ok, json.dumps(mod))
                    self.publish(self.ctl_topic, json.dumps(resp))

                # module delete
                if (ctl_msg['action'] == 'delete' and ctl_msg['data']['type'] == 'module'):
                    mod_data = ctl_msg['data']
                    try:
                        self.modules.delete(mod_data['uuid'])
                    except Exception as err:
                        print('Error deleting module:', err)                        
                        resp = ARTSResponse(ctl_msg['object_id'],Result.err, 'Module could not be deleted; {1}'.format(err))
                        self.publish(self.ctl_topic, json.dumps(resp))
                        return                      
                    print('Sending Confirmation!')
                    resp = ARTSResponse(ctl_msg['object_id'],Result.ok, { "msg": "Deleted.", "uuid" : mod_data['uuid'] })
                    self.publish(self.ctl_topic, json.dumps(resp))                    
        
    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def start(self, host):
        print('Connecting to:', host)
        # register last will
        self.will_set(self.reg_topic, str(RuntimeView().json_unreg(uuid.uuid4(), self.runtime)), 0, False)        
        self.connect(host, 1883, 60)    
        # subscribe to reg topic     
        self.subscribe(self.reg_topic)
        self.loop_start()
        
                