import sys
from pyo import *
import time
import random

s = Server(sr=48000, buffersize=256, duplex=0, winhost="wasapi").boot().start()
s.amp = 0.1

# LFO types:
# 0. Saw up
# 1. Saw down
# 2. Square
# 3. Triangle
# 4. Pulse
# 5. BiPulse
# 6. Sample and Hold
# 7. Modulated sine

clock = LFO(freq=4, type=2, mul=0.5, add=0.5).out()

# pentatonic scale notes in frequency
scale = [261.63, 293.66, 329.63, 392.00, 440.00, 493.88, 523.25]

# pluck synth
pluck_env = Adsr(attack=0, decay=0.2, sustain=0, release=0, dur=0.25, mul=1)
pluck_dry = LFO(freq = 440, type=0, mul=pluck_env)
pluck_wet = Biquad(pluck_dry, freq=100 + pluck_env*2000, q=-(10 + pluck_env), type=0)
pluck_out = pluck_wet.mix(2).out()

check_clock = 0

while True:
    if clock.get == 1 and check_clock == 0:
        pluck_env.play()
        pluck_dry.setFreq(scale[int(random.uniform(0, 6))])
        check_clock = 1
    elif clock.get == 0:
        check_clock = 0
