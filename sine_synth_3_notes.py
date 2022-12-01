#!/usr/bin/env python3
"""Play a sine signal."""
import sys, tty, termios

import numpy as np
import sounddevice as sd

device = 1
start_idx = 0
frequency1 = 0
frequency2 = 0
frequency3 = 0
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

	data = (amplitude * np.sin(3 * 30 * frequency1 * t)) + (amplitude * np.sin(3 * 30 * frequency2 * t)) + (amplitude * np.sin(3 * 30 * frequency3 * t))
	outdata[:] = data
	start_idx += frames

with sd.OutputStream(device=device, channels=1, callback=callback,
						samplerate=samplerate):
	print('#' * 80)
	print('press Enter to quit')
	print('#' * 80)

	print('Enter a single character: ')

	while True:
		user_input = sys.stdin.read(1)[0]

		frequency1 = 0
		frequency2 = 0
		frequency3 = 0

		# if enter pressed exit
		if ord(user_input) == 10:
			break

		if len(user_input) == 1:
			match user_input:
				case 'a':
					amplitude = default_amplitude
					frequency1 = 16.35
					frequency2 = 20.60
					frequency3 = 24.50
				case 's':
					amplitude = default_amplitude
					frequency1 = 18.35
					frequency2 = 21.83
					frequency3 = 27.50
				case 'd':
					amplitude = default_amplitude
					frequency1 = 20.60
					frequency2 = 24.50
					frequency3 = 30.87
				case 'f':
					amplitude = default_amplitude
					frequency1 = 21.83
					frequency2 = 27.50
					frequency3 = 16.35 * 2
				case 'g':
					amplitude = default_amplitude
					frequency1 = 24.50
					frequency2 = 30.87
					frequency3 = 18.35 * 2
				case 'h':
					amplitude = default_amplitude
					frequency1 = 27.50
					frequency2 = 16.35 * 2
					frequency3 = 20.60 * 2
				case 'j':
					amplitude = default_amplitude
					frequency1 = 30.87
					frequency2 = 18.35 * 2
					frequency3 = 20.60 * 2
				case 'k':
					amplitude = default_amplitude
					frequency1 = 16.35 * 2
					frequency2 = 20.60 * 2
					frequency3 = 24.50 * 2
