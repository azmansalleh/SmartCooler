class Frameimage():
    #init class
    def __init__(self):
        self.reset()
     #reset Frame Object into 0 values   
    def reset(self):
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
        self.nameCounter = 0
        self.identity = "Unknown"
        self.identitySound = "Unknown"
    #set Attributes for faceID, gennder, age and smile of a person
    def setAttributes(self,faceID,gender,age,smile):
        self.faceID = faceID
        self.gender = gender.capitalize()
        self.age = age
        self.smile = smile
    #set square frame when it detects the person face
    def setFraming(self,rect):
        self.width = rect['width']
        self.height = rect['height']
        self.top = rect['top']
        self.left = rect['left']
    #Default framing values
    def setDefaultFraming(self):
        if self.frameCounter >= 2:
            self.width = 1000
            self.height = 1000
            self.top = 1000
            self.left = 1000
            self.frameCounter = 0
    #set frame counter
    def setCounter(self):
        self.frameCounter += 1
    #reset frame counter to 0
    def resetCounter(self):
        self.frameCounter = 0
    # #set name counter when it detect a face
    # def setNameCounter(self):
    #     self.nameCounter += 1
    # #get the number of names in the frame 
    # def getNameCounter(self):
    #     return self.nameCounter
    # #reset the number of name counter
    # def resetNameCounter(self):
    #     self.nameCounter = 0
    #return the frame of a dectected face
    def returnFraming(self):
        return (self.width,self.height,self.top,self.left)
    #set the identity of the face detected
    def setIdentification(self,identity):
        self.identity = identity
        self.identitySound = identity
    #get the identity of the person detected
    def getIdentity(self):
        return self.identitySound
    #clear the identity name
    def clearIdentityName(self):        
        self.identitySound = "Unknown"
    #clear the identity sounnd
    def clearIdentitySound(self):
        self.identitySound = "Unknown"
