import json
from flask import Flask

from runtimemngr.modules import ModulesView

app = Flask(__name__)

g_runtime = None
g_modules = None

#class HttpStatus(FlaskView):
    
#    excluded_methods = ['start']
    
def run(rt, mod):
    global g_runtime
    global g_modules
    g_runtime = rt
    g_modules = mod
    app.run()
    
@app.route('/')
def index():
    list =  "<a href='./runtime'>/runtime</a> <br/>"
    list += "<a href='./modules'>/modules</a> <br/>"
    return list

@app.route('/runtime/')
def runtime():
    return json.dumps(g_runtime)

@app.route('/modules/')
def modules():
    
        
    return ModulesView().json_item_list(g_modules)