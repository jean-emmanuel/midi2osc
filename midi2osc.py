#!/usr/bin/env python
#encoding: utf-8
"""
Midi to OSC Router
Copyleft Jean-Emmanuel Doucet (http://ammd.net)
Released under GNU/GPL License (http://www.gnu.org/)
"""

from mididings import *
import liblo as _liblo

# Config

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
    4: '/Transport/Record',
    5: '/Track/Next',
    6: '/Track/Previous',
    7: '/Marker/Set',
    8: '/Marker/Next',
    9: '/Marker/Previous',
   10: '/Transport/Cycle'
}

for s in [1,2,3,4,5,6,7,8]:
    oscPatch[s*10+1]= '/Strip'+str(s)+ '/Fader'
    oscPatch[s*10+2]= '/Strip'+str(s)+ '/Knob'
    oscPatch[s*10+3]= '/Strip'+str(s)+ '/Solo'
    oscPatch[s*10+4]= '/Strip'+str(s)+ '/Mute'
    oscPatch[s*10+5]= '/Strip'+str(s)+ '/Record'


# Prefix

oscPrefix = '/' + oscName


# OSC -> MIDI

class osc2midi(object):
    def __init__(self, port=None):
        self.port = port
        self.patch = dict((oscPatch[k], k) for k in oscPatch)

    def on_start(self):
        if self.port is not None:
            self.server = _liblo.ServerThread(self.port)
            self.server.register_methods(self)
            self.server.start()

    def on_exit(self):
        if self.port is not None:
            self.server.stop()
            del self.server
            
    @_liblo.make_method(None, 'f')
    def sendMidi(self, path, args):
        value = int(max(1,min(0,args[0]))*127)
        if path[len(oscPrefix):] in self.patch and oscPrefix in path:
            Ctrl(self.patch[path[len(oscPrefix):]],value)
        elif oscPrefix+'/CC/' in path:
            Ctrl(int(path.split('/')[-1]),value)
        
# MIDI -> OSC

def routeOsc(e):
    if e.ctrl in oscPatch:
        _liblo.send(oscOutPort, oscPrefix + oscPatch[e.ctrl], e.value / 127.)
    else:
        _liblo.send(oscOutPort, oscPrefix + '/CC/' + str(e.ctrl), e.value / 127.)
        
config(
    backend = midiBackend,
    client_name = 'Midi2osc ' + oscName,
    in_ports=['Midi2oscIn'],
    out_ports=['Midi2oscOut']
)
if feedBackMidi == 1:
    hook(
        osc2midi(port=oscInPort)
    )
run(
    Filter(CTRL) >> Call(routeOsc)
)
