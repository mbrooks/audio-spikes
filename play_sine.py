#!/usr/bin/env python3
"""Play a sine signal."""
import sys

import numpy as np
import sounddevice as sd

device = 1
start_idx = 0
amplitude = 0.2
frequency = 400

samplerate = sd.query_devices(device, 'output')['default_samplerate']

def callback(outdata, frames, time, status):
	if status:
		print(status, file=sys.stderr)
	global start_idx
	t = (start_idx + np.arange(frames)) / samplerate
	t = t.reshape(-1, 1)
	outdata[:] = amplitude * np.sin(2 * np.pi * frequency * t)
	start_idx += frames

with sd.OutputStream(device=device, channels=1, callback=callback,
						samplerate=samplerate):
	print('#' * 80)
	print('press Return to quit')
	print('#' * 80)
	input()
