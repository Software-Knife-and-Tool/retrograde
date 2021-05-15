import json

VERSION = '0.0.1'

def config(dct):
    return

def lumino():
    with open('./lumino/lumino.conf', 'r') as file:
        conf_dict = json.load(file)
        print(json.dumps(_conf_dict))
        config(conf_dict)
    return conf_dict
