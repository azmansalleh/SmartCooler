import cv2
import time
import cognitive_face as CF
import requests
import threading
import multiprocessing
from Frame import *
from Session import *
from Query import *
from PIL import Image
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

smartCooler = Session()
smartCooler.startSession(CF)

demograph = Query()

liquidStudio = CF.person.lists(smartCooler.getGroup())

cap = cv2.VideoCapture(1)
temp = Frameimage()



def camCapture():
	while True:
		ret,frame = cap.read()

		cv2.rectangle(frame, (temp.left, temp.top), (temp.left + temp.width, temp.top + temp.height),(0, 255, 0), 3)
		cv2.putText(frame, '{},{},{}'.format(temp.identity,temp.gender, int(temp.age)), (temp.left, temp.top),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255))

		smartCooler.setWindow(cv2,frame)	
		
		if cv2.waitKey(10) == 27:
			break

def frameProcess():
	while True:
		try:
			result = CF.face.detect("frame.jpg",attributes = "age,gender,smile,emotion,hair")
			if not result:
				temp.setCounter()
				temp.setDefaultFraming()
				print (temp.frameCounter)	

			else:
				for face in result:
					temp.resetCounter()

					#Face Attributes
					faceID = face["faceId"]
					gender = face['faceAttributes']['gender']
					age = face['faceAttributes']['age']
					smile = face['faceAttributes']['smile']
					emotion = face['faceAttributes']['emotion']
					hair = face['faceAttributes']['hair']


					#demograph.create(gender,age,smile,emotion,hair)

					temp.setAttributes(faceID,gender,age,smile)
					#print (emotion)

					#Face rectangle framing
					rect = face['faceRectangle']
					temp.setFraming(rect)
				

			#print ("Gender:",gender,"Age:",age,"Smile:",smile)
			#print ("Width:",temp.width,"Height:",temp.height,"Top:",temp.top,"Left:", temp.left)
			#print ("Identity:", temp.identity)
		except:
			pass
			#while True:
				#print ("Empty")
				
				#print (temp.returnFraming())
			#print ("Framing shot...")

		

def faceIdentify():
	while True:
		try:
			faceArray = []
			faceArray.append(temp.faceID)

			for person in liquidStudio:
				verifyPerson = CF.face.verify(temp.faceID,None,smartCooler.getGroup(),None,person["personId"])
				if verifyPerson["isIdentical"] == True:
					temp.setIdentification(person["name"])
				#else:
					#temp.setIdentification("What's this Pokemon?")
		except:
			pass
			#print ("Not identified")
		
if __name__ == '__main__':

	thread1 = threading.Thread(target=camCapture)
	thread2 = threading.Thread(target=frameProcess)
	thread3 = threading.Thread(target=faceIdentify)

	thread1.start()
	thread2.start()
	thread3.start()

	thread1.join()
	thread2.join()
	thread3.join()

	cap.release()
	cv2.destroyAllWindows()  # destroy all the opened window