class Switch():
	def __init__(self,serial):
		self.reset(serial)
		
	def reset(self,serial):
		self.port = "COM3"
		self.rate = 9600
		self.arduino = serial.Serial(self.port, self.rate, timeout=.1)	
		self.door = "Closed"

	def read(self):
		while 1:
			#self.data = self.arduino.readline()[:-2].decode('utf-8')
			self.data = self.arduino.readline()[:-2].decode('cp1252')
			return self.data

	def openDoor(self):
		self.door = "Opened"

	def closeDoor(self):
		self.door = "Closed"

	def checkDoor(self):
		return self.door
