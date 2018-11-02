#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

try:
	id, data= reader.read()
	print(id)
finally:
	GPIO.cleanup()
