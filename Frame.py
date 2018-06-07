class Frameimage():
    def __init__(self):
        self.faceID = 0
        self.gender = 0
        self.age = 0
        self.smile = 0
        self.faces = 0
        self.width = 0
        self.height = 0
        self.top = 0
        self.left = 0
        self.frameCounter = 0
        self.identity = "Searching....."

    def setAttributes(self,faceID,gender,age,smile):
        self.faceID = faceID
        self.gender = gender.capitalize()
        self.age = age
        self.smile = smile

    def setFraming(self,rect):
        self.width = rect['width']
        self.height = rect['height']
        self.top = rect['top']
        self.left = rect['left']

    def setDefaultFraming(self):
        if self.frameCounter >= 2:
            self.width = 1000
            self.height = 1000
            self.top = 1000
            self.left = 1000
            self.frameCounter = 0

    def setCounter(self):
        self.frameCounter += 1

    def resetCounter(self):
        self.frameCounter = 0

    def returnFraming(self):
        return (self.width,self.height,self.top,self.left)

    def setIdentification(self,identity):
        self.identity = identity

    def clearIdentification(self):
        self.identity = "Searching....."