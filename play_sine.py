#!/usr/bin/env python3
"""Play a sine signal."""
import sys, tty, termios

import numpy as np
import sounddevice as sd

device = 1
start_idx = 0
amplitude = 0.2
frequency = 440

filedescriptors = termios. tcgetattr(sys. stdin)
tty. setcbreak(sys. stdin)

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


	while True:
		print('Enter a single character: ')
		user_input = sys.stdin.read(1)[0]

		if len(user_input) == 1:
			match user_input:
				case 'a':
					frequency = 440
				case 's':
					frequency = 500
				case 'd':
					frequency = 560
				case 'f':
					frequency = 600
				case 'g':
					frequency = 680
				case 'h':
					frequency = 760
				case 'j':
					frequency = 840
				case 'k':
					frequency = 880

		elif user_input == '':
			break

		else:
			print('Enter a single character to continue.')
			continue