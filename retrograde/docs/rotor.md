#### _Rotor Programming_

------

A _rotor_ is a list of rotor operations executed by the rotor thread. Rotors are coded in _json_, nominally defined in:

```
retrograde/gra_afch/gra_afch.conf
```

Rotors are defined as either a _block_ or a _loop_.

_loops_ execute forever.

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



```
{ "gra-afch": {"delay": INT } }
```

Delay for INT milliseconds, reschedules the rotor thread.



```
{ "repeat": { "count": INT, "block": [...] } }
```

Execute rotor _count_ times.



```
{ "block": [...] } 
{ "loop": [...] }
```

Execute anonymous rotor definition.



###### _Display Operations_:

------



```
{ "back": [R, G, B] }
{ "back": STR }
```

Assign the back light color from an RGB triple or hex string. Color values are in the range 0..255.



```
{ "blank": BOOL }
```

 Power down the entire display. Individual lamps may be blanked with the _mask_ primitive.



```
{ "dots": BOOL }        
```

The display has a pair of indicator lamps, located between tubes 2 and 3 and between 4 and 5. These are enabled/disabled by the argument.

_add individual masks for left/right indicators_



```
{ "mask": INT } 
```

Set the lamp blanking mask, range is _0..255_. Bits _0_ and _6_ are the indicator lamp enables.

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



###### _Display Stack operations_:

------



```
{ "display": STR }              
```

Light lamps from STR.


```
{ "date-time": STR }                     
```

Display formatted date/time. The format string is interpreted as if by _strftime_().



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

7. display the formatted time in a loop at one second intervals

   

```
    "rotors": {
        "default":
          { "event": { "exec": { "block": [
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
              { "event": { "exec": { "loop": [
                  { "gra-afch": { "exec": { "date-time": "%H%M%S" } } },
                  { "gra-afch": { "exec": { "delay": 1000 } } }
              ]}}}
          ]}}}
    }

```













