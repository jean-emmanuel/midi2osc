midi2osc
========

Generic Midi to OSC Router

-----------------

midi2osc converts midi control changes to osc messages

```
midiBackend = 'alsa'    # jack or alsa
feedBackMidi = 0        # monitor oscInPort to send Midi CC to the device
oscOutPort = 3333       # output port
oscInPort = 3334        # input port (used to control the midi device with osc messages)
oscName = 'nanoKontrol' # all osc messages begin with /oscName

# oscPatch = dict(CTRL_NUMBER, 'OSC_PATH')
# Midi CC -> oscOutPort /oscName/OSC_PATH [value*]  *between 0 and 1
# oscinPort /oscName/OSC_PATH [value*] -> Midi CC   *between 0 and 1
oscPatch = {    
    0: '/Transport/Backward',
    1: '/Transport/Forward',
    2: '/Transport/Stop',
    3: '/Transport/Play',
    4: '/Transport/Record'
}
```

- once running, the router must be connected to the appropriate midi device using a patchbay such as qjackctl



# Dependances

- jack
- mididings
- liblo
