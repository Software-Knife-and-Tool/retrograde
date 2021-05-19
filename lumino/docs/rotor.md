_rotor language_:

 name: str         rotor name
 _ops_:
     rotors:
         delay: _int_          delay for millisecs
         repeat: { count: int, rotor: [...]
                                    repeat rotor _count_ times
     rotor: [...]               anonymous rotor definition
     stop:                      stop rotor/pop rotor stack

 _display_:
     back: [r, g, b]       backlight color
     blank: _true_|_false_  turn on/off tube power
     date: _str_                 stuff formatted date to tubes
     dots: _true_|_false_    enable/disable dots
     mask: _int_                bit mask for tubes [0..255]
     time: _str_                  stuff formatted time onto tubes

 _tube stack_:
     display: _null_           stuff top of _tubes_stack_ onto tubes
     pop: _null_                pop _tubes_stack_
     push: _str_                 push digit string on __tubes_stack_

 _json_:
     "rotors" : {
         "name" : {
                           "op": ...,
                         },