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

ADD_ECHO = True

filedescriptors = termios. tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)

samplerate = sd.query_devices(device, 'output')['default_samplerate']

class Note():
	def __init__(self, frequency) -> None:
		self.amplitude = 0.5
		self.frequency = frequency

	def get(self):
		return [self.amplitude, self.frequency]

def decayAmplitude(note):
	decay = 0.97
	amplitude = note[0] * decay
	return [amplitude, note[1]]

def filterNote(note):
	amplitude = note[0] * decay
	if amplitude < 0.0001:
		return False
	return True

class Delay():
	def __init__(self):
		self.delayArray1 = [np.zeros([512, 1])] * 10
		self.delayArray2 = [np.zeros([512, 1])] * 13

	def process(self, input):
		self.delayArray1.append(input)
		self.delayArray2.append(input)
		one = self.delayArray1.pop(0) * .80
		two = self.delayArray2.pop(0) * .75
		return one + two

class NoteCollection():
	def __init__(self):
		self.notes = []
		self.default_amplitude = 0.5

	def add(self, frequency):
		self.notes.append([default_amplitude, frequency])

	def getAll(self):
		self.notes = list(filter(filterNote, map(lambda note: decayAmplitude(note), self.notes)))
		return self.notes

notecollection = NoteCollection()
delay = Delay()

def callback(outdata, frames, time, status):
	if status:
		print(status, file=sys.stderr)

	global start_idx, amplitude, notecollection
	notes = notecollection.getAll()
	t = (start_idx + np.arange(frames)) / samplerate
	t = t.reshape(-1, 1)

	out = np.empty([512, 1])
	for note in notes:
		out = out + (note[0] * np.sin(3 * 30 * note[1] * t))

	if ADD_ECHO:
		out = out + delay.process(out)

	outdata[:] = out
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
			note = None
			match user_input:
				case 'a':
					note = 16.35
				case 's':
					note = 18.35
				case 'd':
					note = 20.60
				case 'f':
					note = 21.83
				case 'g':
					note = 24.50
				case 'h':
					note = 27.50
				case 'j':
					note = 30.87
				case 'k':
					note = 16.35 * 2
			if note:
				notecollection.add(note)
