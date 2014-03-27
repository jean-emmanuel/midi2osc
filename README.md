midi2osc
========

Generic Midi to OSC Router

-----------------

midi2osc converts midi control changes to osc messages

- the osc messages can be defined for each midi control number in the variable oscPatch (dictionnary) :
```
oscPatch = {    
    0: '/Transport/Backward',
    1: '/Transport/Forward',
    2: '/Transport/Stop',
    3: '/Transport/Play',
    4: '/Transport/Record'
}
```
- osc message will be '/oscName/Transport/Record 1' for a midi CC (controler=4, value=127)
- midi values from 0 to 127 are mapped between 0.0 and 1.0
- once running, the router must be connected to the appropriate midi device using a patchbay such as qjackctl
- feedBackMidi can be set to 1 in order to convert osc messages sent to router into midi control changes sent to the device



# Dependances

- jack
- mididings
- liblo
