import json
# import grafch

_conf_dict = None

def lumen():
    with open('./lumino.conf', 'r') as file:
        _conf_dict = json.load(file)
        print(json.dumps(conf_dict))
    return _conf_dict
    
def version():
    return '0.0.1'
