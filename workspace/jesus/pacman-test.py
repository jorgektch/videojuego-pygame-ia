import sys
from pyo import *
import time

s = Server(sr=48000, buffersize=256, duplex=0, winhost="wasapi").boot()

globalamp = Fader(fadein=0, fadeout=0, dur=0).play()

lfo_freq = 3 

lfo_1 = LFO(freq=lfo_freq, sharp=0.5, type = 3, mul=-100, add=100) # controla frecuencia
env = Adsr(attack=0.01, decay=0.1, sustain=0.0, release=0.0, dur=0.5, mul=0.5)

tone = LFO(freq=lfo_1 + 20, sharp=1, type = 4, mul=0.15*env*globalamp).mix(2).out()

s.start()

env.play()

s.stop