#import serial

#toggle swtich open or close

class Switch():
	def __init__(self,serial):
		self.reset(serial)
		
	def reset(self,serial):
		self.port = "COM5"
		self.rate = 9600
		self.arduino = serial.Serial(self.port, self.rate, timeout=.1)	
		self.door = "Closed"

	def read(self):
		while 1:
			self.data = self.arduino.readline()[:-2].decode('utf-8')
			return self.data

	def openDoor(self):
		self.door = "Opened"

	def closeDoor(self):
		self.door = "Closed"

	def checkDoor(self):
		return self.door
		

# #test.printme()
# #print (test.testme())
