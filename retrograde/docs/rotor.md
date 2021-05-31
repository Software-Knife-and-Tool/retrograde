#### _Rotor Programming_

------

A _rotor_ is a list of rotor operations executed by the rotor thread. Rotors are coded in _json_, nominally defined in:

```
retrograde/gra_afch/gra_afch.conf
```

Rotors are defined as a _block_.

_blocks_ stop executing at the end of the definition.


###### _Operations Summary_

------


###### Control flow: _delay repeat block loop_

###### Display: _back blank dots mask_ 

###### Display stack:  _display date-time_



###### _Rotor definitions_:

------



```
"rotors" : {
             "name" : {
                        { "op": ... },
                      },
           }           
```



###### _Rotor name_:

------



```
{ "name": STR }
```

Bind rotor definition to STR.



###### _Rotor operations_:  

------

Rotor operations are expressed as events. An _event_ is a JSON object structured as:

```
{ MODULE: { EVENT: ARG } }
```

where

MODULE: "event", "retro", "gra-afch", "integration"

EVENT:  "button", "timer", "alarm", "ui-control", "integration", "exec"

ARG:    context-based object



Rotor operations are a special case of a general event, their EVENT type is "exec". Control flow operations are managed by the _event_ module, NCS31X operations are managed by the "gra-afch"' module, and UI and system operations are managed by the "retro" module.



```
{ "gra-afch": {"exec": { "delay": INT } } }
```

Delay for INT milliseconds, reschedules the rotor thread.



```
{ "event": { "exec": { repeat": { "count": INT|BOOL, "block": [...] } } }
```

Execute operation block _count_ times. _count_ may be an int, or a bool. If _count_ is true, the block will be repeated forever, if false, never.



```
{ "event": { "exec": { "block": [...] } } }

```

Execute anonymous block.



###### _Display Operations_:

------

Display operations are implemented by the _gra-afch_ module.



```
{ "gra-afch": { "exec": { "back": [R, G, B] } } }
{ "gra-afch": { "exec": { "back": STR } } }
```

Assign the back light color from an RGB triple or hex string. Color values are in INTs in the range _[0..255]_.



```
{ "gra-afch": { "exec": { "blank": BOOL } } }
```

 Power down the entire display. Individual lamps may be blanked with the _mask_ primitive.



```
{ "gra-afch": { "exec": { "dots": BOOL } } }
```

The display has a pair of indicator lamps, located between tubes 2 and 3 and between 4 and 5. These are enabled/disabled by the argument.

_add individual masks for left/right indicators_



```
{ "gra-afch": { "exec": { "mask": INT } } }
```

Set the lamp blanking mask, range is _[0..255]_. Bits _0_ and _6_ are the indicator lamp enables.

| bit # | enable mask              | adjacency mask* (left, right) |
| ----- | ------------------------ | ----------------------------- |
| 0     | 1 - right indicator lamp | 1, 255                        |
| 1     | 2 - lamp 0 (rightmost)   | 2, 254                        |
| 2     | 4 - lamp 1               | 6, 252                        |
| 3     | 8 - lamp 2               | 14, 248                       |
| 4     | 16 - lamp 3              | 30, 240                       |
| 5     | 32 - lamp 4              | 62, 224                       |
| 6     | 64 - left indicator lamp | 126, 192                      |
| 7     | 128 - lamp 5 (leftmost)  | 254, 128                      |

\* - _and_ in indicator lamp enables



```
{ "gra-afch": { "exec": { "display": STR } } }
```

Light lamps from STR. STR is a decimal numeric string of six digits.




```
{ "gra-afch": { "exec": { "date-time": STR } } }                 
```

Display formatted date/time. The format STR is interpreted as if by _strftime_().



###### Example:

------

This is the default rotor definition, which runs on startup.

1. assigns an orange color to the back light

2. turn off the indicator lamps

3. display a fixed digit string

4. mask the display off and then on after a short delay

5. repeat three times:

   1. display the formatted date
   2. blank and unblank the display for a brief period

6. blank the display for a brief period

7. display the formatted time in a loop at 200ms intervals

   

```
 
   "rotors": {
        "default":
          { "event": { "exec": { "block": [
              { "gra-afch": { "exec": { "sync": null } } },
              { "gra-afch": { "exec": { "back": [ 255, 32, 0 ] } } },
              { "gra-afch": { "exec": { "dots": false } } },
              { "gra-afch": { "exec": { "display": "000001" } } },
              { "gra-afch": { "exec": { "delay": 1000 } } },
              { "gra-afch": { "exec": { "mask": 0 } } },
              { "gra-afch": { "exec": { "delay": 1000 } } },
              { "gra-afch": { "exec": { "mask": 255 } } },    
              { "event":    { "exec": { "repeat": { "count": 3,
                                                    "block": [
                                                        { "gra-afch": { "exec": { "date-time": "%m%d%y" } } },
                                                        { "gra-afch": { "exec": { "delay": 500 } } },
                                                        { "gra-afch": { "exec": { "blank": true } } },
                                                        { "gra-afch": { "exec": { "delay": 500 } } },
                                                        { "gra-afch": { "exec": { "blank": false } } }
                                                    ]}}}},
              { "gra-afch": { "exec": { "blank": true } } },
              { "gra-afch": { "exec": { "delay": 1000 } } },
              { "gra-afch": { "exec": { "blank": false } } },
              { "event":    { "exec": { "repeat": { "count": true,
                                                    "block": [
                                                        { "gra-afch": { "exec": { "date-time": "%H%M%S" } } },
                                                        { "gra-afch": { "exec": { "delay": 200 } } }
                                                    ]}}}}
              ]}}}
    }

```













