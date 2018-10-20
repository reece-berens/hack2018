import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

class DistanceSensor:
	def __init__(self, name, echoPin, triggerPin):
		self.name = name
		self.echoPin = echoPin
		self.triggerPin = triggerPin
		GPIO.setup(self.triggerPin, GPIO.OUT)
		GPIO.setup(self.echoPin, GPIO.IN)
		GPIO.output(self.triggerPin, False)
	
	def getDistance(self):
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
		
		distance = TimeElapsed * 17150
		distance = round(distance, 2)
		
		return distance
		
class Button:
	def __init__(self, name, buttonPin):
		self.name = name
		self.pin = buttonPin
		GPIO.setup(self.pin, GPIO.input, pull_up_down = GPIO.PUD_UP)
		
	def getButtonState(self):
		state = GPIO.input(self.pin)
		if state == False:
			return False
		else:
			return True
		    
"""		    
if __name__ == '__main__':
    sensor = DistanceSensor('left', 13, 11)
    #time.sleep(1)
    while True:
        value = sensor.getDistance()
        print("Value is {}".format(value))
        #time.sleep(.8)
"""