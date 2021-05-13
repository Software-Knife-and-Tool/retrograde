import os
import select
import json

import grafch

# import emb
# print("Number of arguments", emb.numargs())

def event(id):
    print(f'{{ "event": {id}" }}')
    
def command(cmd_dict):
    print(json.dumps(cmd_dict))
    if 'event' in cmd_dict:
        cmd = cmd_dict['event']
        utf8 = cmd.encode('utf-8')
        event(utf8)
        return
    if 'grafch' in cmd_dict:
        cmd = cmd_dict['grafch']
        # short command
        if type(cmd) is unicode:
            utf8 = cmd.encode('utf-8')
            if utf8 == 'time':
                return
            if utf8 == 'date':
                return
            if utf8 == 'blank':
                return
            if utf8 == 'unblank':
                return
            if utf8 == 'return':
                return
            return

        # extended command
        if type(cmd_dict['grafch']) is dict:
            if 'delay' in cmd:
                delay = cmd['delay']
                return
            if 'tube' in cmd:
                tube = cmd['tube']
                state = cmd['state']
                return
            if 'digit' in cmd:
                tube = cmd['digit']
                value = cmd['value']
                return
            if 'rotor' in cmd:
                rotor = cmd['rotor']
                return

def init():
    inpath = '/var/tmp/to-grafch'
    outpath = '/var/tmp/from-grafch'
    
    # read config
    with open('/opt/grafch/grafch-daemon.conf', 'r') as file:
        conf_dict = json.load(file)
        print(json.dumps(conf_dict))
        if 'pipe-in' in conf_dict:
            inpath = conf_dict['pipe-in'].encode('utf-8')
        if 'pipe-out' in conf_dict:
            outpath = conf_dict['pipe-in'].encode('utf-8')
            
    # attach pipes
    if not(os.path.exists(inpath)):
        os.mkfifo(inpath)
    inpipefd = os.open(inpath, os.O_RDONLY | os.O_NONBLOCK);
    inpipefile = os.fdopen(inpipefd, 'r');

    # command loop
    while True:
        select.select([inpipefile.fileno()],[],[])
        command(json.load(inpipefile))
    
init()
