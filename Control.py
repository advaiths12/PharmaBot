import RPi.GPIO as GPIO
import time
import string
from smtp import notify

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12,50)
p.start(3.5)
#stack for servos
#queue for task execution, separate from checking
#GUI
# 37 degrees of incline for dispenser
class Pill(object):
    def __init__ (self,name, time, number, servo = 0):
        self.name = name
        self.time = time
        self.number = number
	self.parity = 0
	self.dispensed = 0
	self.servo = servo

    def __eq__(self, other):
        return (isinstance(other, Pill) and \
                    self.name == other.name and \
                    self.time == other.time and self.number == other.number)
                    
                    
    def timing(self, timein):
        if(timein.tm_hour == self.time[0] and timein.tm_min == self.time[1] and timein.tm_sec == 0):
            return True
        else:
            return False

def dispense(servo, parity):
    if(parity % 2 == 0):
	p.ChangeDutyCycle(7.5)
    	time.sleep(.5)
	
    else:
	print("other way")
	p.ChangeDutyCycle(3.5)
	time.sleep(.5)
	
	


H = dict()
disp = raw_input("How many modules?")
for i in range(int(disp)):
	namex = raw_input(" Enter a pill name: ")
        hourin = int(raw_input("enter the hour of day "))
        minutein = int(raw_input("enter the minute of day "))
        freq = raw_input("enter number of pills ")
	addr = raw_input("enter email address: ")
        timearr = [hourin, minutein]

        pill = Pill(namex,timearr, freq)	 
        H[i] = pill
	
for pill in H:
	print("name:", H[pill].name, "time:", H[pill].time, "freq", H[pill].number)
	
try:
    
    while True:
	 for entry in H:
        	if(H[entry].timing(time.localtime()) and H[entry].dispensed < H[entry].number ):
			print("entered")
                	print("DISPENSE", H[entry].name)
			print("name:", H[pill].name, " time:", H[pill].time)
			notify(H[entry], addr)
			print("SENT NOTIFICATION")
			for i in range(int(H[entry].number)):
                		dispense(p, H[entry].parity)
			
				H[entry].dispensed += 1
				H[entry].parity = 0 if H[entry].parity else 1 
				print("parity change", H[entry].parity)
          


except KeyboardInterrupt:
	for pill in H:
		print("name:", H[pill].name, "time:", H[pill].time, "dispensed", H[pill].dispensed)
	
	p.stop()
	GPIO.cleanup()
