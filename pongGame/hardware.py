import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class DistanceSensor:
	def __init__(name, echoPin, triggerPin):
		self.name = name
		self.echoPin = echoPin
		self.triggerPin = triggerPin
		GPIO.setup(self.triggerPin, GPIO.OUT)
		GPIO.setup(self.echoPin, GPIO.IN)
	
	def getDistance():
		GPIO.output(self.triggerPin, True)
		time.sleep(.00001)
		GPIO.output(self.triggerPin, False)
		
		StartTime = time.time()
		StopTime = time.time()
		
		while GPIO.input(self.echoPin) == 0:
			StartTime = time.time()
		while GPIO.input(self.echoPin) == 1:
			StopTime = time.time()
			
		TimeElapsed = StopTime - StartTime
		
		distance = (TimeElapsed * 34300) / 2
		
		return distance
		
class Button:
	def __init__(name, buttonPin):
		self.name = name
		self.pin = buttonPin
		GPIO.setup(self.pin, GPIO.input, pull_up_down = GPIO.PUD_UP)
		
	def getButtonState():
		state = GPIO.input(self.pin)
		if state == False:
			return False
		else:
			return True