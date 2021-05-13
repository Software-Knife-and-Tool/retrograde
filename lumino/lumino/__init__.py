import json

_conf_dict = None

def lumino():
    with open('./lumino/lumino.conf', 'r') as file:
        _conf_dict = json.load(file)
        print(json.dumps(_conf_dict))
    return _conf_dict
    
def version():
    return '0.0.1'
