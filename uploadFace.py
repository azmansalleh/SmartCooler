import cognitive_face as CF
import requests
from Session import *

from requests.packages.urllib3.exceptions import InsecureRequestWarning


session = Session()
session.startSession(CF)

group = "liquidstudiosg"
name = "Aster"
mobile = "82011037"
face_link = "Faces/aster.jpg"
personID = "b6343810-ac7b-4574-9cdd-c233a6801b3f"

#CF.person.create(group,name,mobile)
CF.person.add_face(face_link,group,personID)

