#creates a session to use the face API from mircosoft 

class Session():
	def __init__(self):
		self.reset()
		
	def reset(self):
		self.window = "Smart Cooler"
		self.img = "frame.jpg"
		self.url = "https://southeastasia.api.cognitive.microsoft.com/face/v1.0"
		self.key = "f2378de47ace413bbf4dd2538745c40b"
		self.groupID = "liquidstudiosg"

		self.nameCounter = 0
		self.verification = False
		self.switch = True
		self.verificationTime = 0
		
	def startSession(self,CF):
		CF.BaseUrl.set(self.url)
		CF.Key.set(self.key)

	def setWindow(self,cv2,frame):
		cv2.imshow('Smart Fridge',frame)
		cv2.imwrite("frame.jpg", frame)	

	def getGroup(self):
		return self.groupID

	def welcomeName(self,time,PG,name):
		if self.nameCounter == 0:
			self.nameSound = PG.mixer.Sound("audio/"+name+".wav")
			self.restockSound = PG.mixer.Sound("audio/test.wav")
			self.nameSound.play()
			time.sleep(3.5)
			self.restockSound.play()
			self.nameCounter +=1

	def verified(self):
		self.verification = True
		self.verificationTime += 1	

	def checkVerification(self):
		return self.verification

	def clearVerification(self):
		self.verification = False

	def getCounter(self):
		return self.nameCounter
		


