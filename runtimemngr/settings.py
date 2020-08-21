import json

class Settings():

    def __init__(self, cfg_file):
        with open(cfg_file) as json_data_file:
            self.s_dict = json.load(json_data_file)

        for t in self.s_dict['topics']:
            if (t['type'] == 'reg'):
                self.reg_topic = t['topic']
            if (t['type'] == 'ctl'):
                self.ctl_topic = t['topic']
            if (t['type'] == 'dbg'):
                self.dbg_topic = t['topic']        
