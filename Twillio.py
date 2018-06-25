# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import random
import time

class Twillio():
	def __init__(self):
		self.account_sid = 'ACd1cbc8fe8d00479adbd65397ac1dbe00'
		self.auth_token = '3f22efedfc21e1e394c72cdf7cc7369c'
		self.client = Client(self.account_sid, self.auth_token)
		self.otp = random.randint(1000, 9999)
		self.mobile = ""

	def message(self):
		
		self.message = self.client.messages.create(
                              body='Your OTP is ' +  str(self.otp),
                              from_='(646)571-0768',
                              to=self.mobile
                          )
		print ("Done")

	def setMobile(self,number):
		self.mobile = "+65" + str(number)

	def getOTP(self):
		return self.otp

#sms = Twillio()
# sms.message()
# print(sms.getOTP())
#print (sms.otp)

	