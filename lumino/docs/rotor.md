#### _Rotor Programming_

A _rotor_ is a list of rotor operations executed by a rotor thread. Rotors are coded in _json_, nominally defined in:

```
lumino/gra_afch/gra_afch.conf
```

Rotors execute in an implicit loop; they continue to execute until they see a _stop_ primitive. Tube lamp contents are maintained and manipulated on a stack. A per-tube blanking bit mask is provided to allow a primitive form of animation.

Active rotors are maintained on an implicit _rotor stack_ to allow nesting and event displays.



###### _Rotor definitions_:

```
"rotors" : {
             "name" : {
                        { "op": ... },
                      },
           }           
```



###### _Rotor name_:

```
{ "name": STR }
```

Bind rotor definition to STR.



###### _Rotor operations_:  

```
{ "delay": INT }
```

Delay for INT milliseconds, reschedules the rotor thread.

```
{ "repeat": { "count": INT, "rotor": [...] }
```

Repeat rotor _count_ times.

```
{ "rotor": [...] } 
```

Push anonymous rotor definition on the _rotor stack_.

```
{ stop: NULL }                  
```

Stop the current rotor and pop the _rotor stack_.



###### _Lamp operations_:

```
{ "back": [R, G, B] } 
```

Assign the back light color to an RGB triple. Color values are in the range 0..255.

_add hex string argument_

```
{ "blank": BOOL }
```

 Powers down the entire display. Individual tubes may be blanked with the _mask_ primitive.

```
{ "dots": BOOL }        
```

The tube display has a pair of indicator lamps, located between tubes 2 and 3 and between 4 and 5. These are enabled/disabled by the argument.

_add individual masks_

```
{ "mask": INT } 
```

Set the lamp blanking mask, range is 0..255. Bits 0 and 6 are the indicator lamps.



###### _Tubes Stack operations_:

```
{ "display": NULL }              
```

Light tubes from the top of the _tubes stack_. The argument is ignored.

```
{ "pop": NULL }                     
```

Pop the _tubes stack_. The argument is ignored.

```
{ "push": STR }                    
```

Push digit string onto the _tubes stack_.

```
{ "date": STR }                     
```

Push formatted date onto the _tubes stack_.

```
{ "time": STR }                      
```

Push formatted time onto the _tubes stack_



###### Futures:

- [ ] Arithmetic operations
- [ ] Logic operations
- [ ] Conditional stop

If we do this, we can claim to be Turing complete.



###### Example:

This is the default rotor definition, which runs on startup.

1. assigns an orange color to the back light

2. turns off the indicator lamps

3. displays a fixed digit string

4. masks the tube display off and then on after a short delay

5. repeats three times:

   1. displays the formatted date
   2. blanks and unblanks the display for a brief period

6. blanks the display for a brief period

7. displays the time at one second intervals

   

```
"rotors": {
            "default": [
                         { "back": [ 255, 32, 0 ] },
                         { "dots": false },
                         { "push": "000001" },
                         { "display" : null},
                         { "delay": 1000},
                         { "mask": 0 },
                         { "pop": null},
                         { "delay": 1000},
                         { "mask": 255 },    
                         { "repeat": { "count": 3,
                                       "rotor": [
                                                  { "date": "%m%d%y" },
                                                  { "display": null },
                                                  { "pop": null },
                                                  { "delay": 500 },
                                                  { "blank": true },
                                                  { "delay": 500 },
                                                  { "blank": false },
                                                  { "stop": true }
                                                ]}},
                         { "blank": true },
                         { "delay": 1000 },
                         { "blank": false },
                         { "rotor": [
                                      { "time": "%H%M%S" },
                                      { "display": null },
                                      { "pop": null },
                                      { "delay": 1000 }
                                    ]}
                 ]
          }
```













