import json

CFG_FILE = 'config.json'

class Settings():
    s_dict = {}    
    reg_topic = ''
    ctl_topic = ''
    dbg_topic = ''
    
    @staticmethod
    def load():
        with open(CFG_FILE) as json_data_file:
            Settings.s_dict = json.load(json_data_file)

        for t in Settings.s_dict['topics']:
            if (t['type'] == 'reg'):
                Settings.reg_topic = t['topic']
            if (t['type'] == 'ctl'):
                Settings.ctl_topic = t['topic']
            if (t['type'] == 'dbg'):
                Settings.dbg_topic = t['topic']        
