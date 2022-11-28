#!/usr/bin/env python3
"""Play a sine signal."""
import sys, tty, termios

import numpy as np
import sounddevice as sd

device = 1
start_idx = 0
frequency = 0
amplitude = 0

default_amplitude = 0.5

decay = 0.97

filedescriptors = termios. tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)

samplerate = sd.query_devices(device, 'output')['default_samplerate']

def callback(outdata, frames, time, status):
	if status:
		print(status, file=sys.stderr)
	global start_idx, amplitude

	# decay amplitude
	amplitude = amplitude * decay

	t = (start_idx + np.arange(frames)) / samplerate
	t = t.reshape(-1, 1)

	outdata[:] = amplitude * np.cos(3 * 30 * frequency * t)
	start_idx += frames

with sd.OutputStream(device=device, channels=1, callback=callback,
						samplerate=samplerate):
	print('#' * 80)
	print('press Enter to quit')
	print('#' * 80)

	print('Enter a single character: ')

	while True:
		user_input = sys.stdin.read(1)[0]

		# if enter pressed exit
		if ord(user_input) == 10:
			break

		if len(user_input) == 1:
			match user_input:
				case 'a':
					amplitude = default_amplitude
					frequency = 16.35
				case 's':
					amplitude = default_amplitude
					frequency = 18.35
				case 'd':
					amplitude = default_amplitude
					frequency = 20.60
				case 'f':
					amplitude = default_amplitude
					frequency = 21.83
				case 'g':
					amplitude = default_amplitude
					frequency = 24.50
				case 'h':
					amplitude = default_amplitude
					frequency = 27.50
				case 'j':
					amplitude = default_amplitude
					frequency = 30.87
				case 'k':
					amplitude = default_amplitude
					frequency = 16.35 * 2
