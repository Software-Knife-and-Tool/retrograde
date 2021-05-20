#### _Rotor Programming_

------

A _rotor_ is a list of rotor operations executed by a rotor thread. Rotors are coded in _json_, nominally defined in:

```
lumino/gra_afch/gra_afch.conf
```

Rotors are defined as either a _block_ or a _loop_. Active rotors are maintained on an implicit _rotor stack_ to allow nesting and event displays.

_Loops_ execute repeatedly until terminated with a _return_ operation.

_Blocks_ stop executing at the end of the definition or otherwise terminated by a _return_ operation.

Lamp contents are maintained and manipulated on the _display stack_. A per-lamp blanking bit mask allows a primitive form of animation.



###### _Operations Summary_

------



###### Control flow: _delay repeat block loop return return?_

###### Display: _back blank dots mask_ 

###### Display stack:  _display dup pop push inc shift date-time_



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
{ "delay": INT }
```

Delay for INT milliseconds, reschedules the rotor thread.



```
{ "repeat": { "count": INT, "block": [...] } }
{ "repeat": { "count": INT, "loop": [...] } }
```

Execute rotor _count_ times.



```
{ "block": [...] } 
{ "loop": [...] }
```

Push anonymous rotor definition on the _rotor stack_.



```
{ return: NULL }
{ "return?": NULL }
```

Stop executing the current rotor and pop the _rotor stack_.



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
{ "display": INT }              
```

Light lamps from the INT _th_ element of the _display stack_.



```
{ "dup": NULL }
```

Duplicate the top of _display stack._



```
{ "pop": INT }                     
```

Pop the _display stack_ INT times.



```
{ "push": STR }                    
```

Push string onto the _display stack_.



```
{ "inc": INT }
```

Increment the top of the _display stack_  by INT. Negative values decrement.



```
{ "shift": { dir="left"|"right", count: INT } }
```

Shift the top of the _display stack_ INT characters to the right or left. Added characters are spaces.



```
{ "date-time": STR }                     
```

Push formatted date/time onto the _display stack_. The format string is interpreted as if by _strftime_().



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

7. display the formatted time at one second intervals

   

```
"rotors": {
            "default": [
                         { "back": [ 255, 32, 0 ] },
                         { "dots": false },
                         { "push": "000001" },
                         { "display" : 0 },
                         { "delay": 1000},
                         { "mask": 0 },
                         { "pop": 1 },
                         { "delay": 1000},
                         { "mask": 255 },    
                         { "repeat": { "count": 3,
                                       "block": [
                                                  { "date-time": "%m%d%y" },
                                                  { "display": 0 },
                                                  { "pop": 1 },
                                                  { "delay": 500 },
                                                  { "blank": true },
                                                  { "delay": 500 },
                                                  { "blank": false },
                                                  { "stop": true }
                                                ]}},
                         { "blank": true },
                         { "delay": 1000 },
                         { "blank": false },
                         { "loop": [
                                      { "date-time": "%H%M%S" },
                                      { "display": 0 },
                                      { "pop": 1 },
                                      { "delay": 1000 }
                                    ]}
                 ]
          }
```













