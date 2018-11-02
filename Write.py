#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

try:
	text = raw_input('New data:')
	print('give data')
	reader.write(text)
	print('Written')
finally:
	GPIO.cleanup()
