class Session():
	def __init__(self):
		self.window = "Smart Cooler"
		self.img = "frame.jpg"
		self.url = "https://southeastasia.api.cognitive.microsoft.com/face/v1.0"
		self.key = "f2378de47ace413bbf4dd2538745c40b"
		self.groupID = "liquidstudiosg"
		self.verification = False

	def startSession(self,CF):
		CF.BaseUrl.set(self.url)
		CF.Key.set(self.key)

	def setWindow(self,cv2,frame):
		cv2.imshow('Smart Fridge',frame)
		cv2.imwrite("frame.jpg", frame)	

	def getGroup(self):
		return self.groupID

	def verified(self):
		self.verification = True

	def checkVerification(self):
		return self.verification
		


