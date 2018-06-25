
## After voice verification

###### Conversation Flow

# Bot: (param) is low on 2, How many would you like to restock?
# Me: 7

## ^ Above should loop until all drinks are restocked (drinks count not less than array size)
## After asking all the drinks...

# Bot: Please confirm the list of items to be restocked: (param) : (qty), (param): (qty)
# Me: Yes/Confirm or No




# > cd C:\Python27\Scripts>
# > pip install pyodbc
import pyodbc

try:
	from urllib.parse import urlparse
except ImportError:
	 from urlparse import urlparse


import requests
import json
import ast
import time
import datetime


initiateAllDrinks = []


global drinksDict
global drinksBelowSafeLevel
global drinksWithinSafeLevel
drinksDict = {}
drinksBelowSafeLevel = {}
drinksWithinSafeLevel = {}

restockingDict = {}

# global currentDT

# http://pymssql.org/en/stable/pymssql_examples.html
# https://blogs.msdn.microsoft.com/cdndevs/2015/03/11/python-and-data-sql-server-as-a-data-source-for-python-applications/
# https://stackoverflow.com/questions/13860026/update-dictionary-with-dynamic-keys-and-values-in-python
def connectDB_retrieveDrinks():
	global drinksBelowSafeLevel
	global drinksWithinSafeLevel
	#pass
	#Connect to azure db
	driver = 'ODBC Driver 17 for SQL Server'
	server = 'tcp:smartcooler3.database.windows.net,1433'
	database = 'smartcooler3'
	uid = 'acn_admin'
	pw = 'Accenture1'
	connection = pyodbc.connect('Driver=' + driver + ';Server=' + server + ';Database=' + database + ';' +'Uid=' + uid + ';Pwd=' + pw)
	# connection = pymssql.connect(server=server, user=uid, password=pw, database=database
	cursor = connection.cursor()
	cursor.execute("SELECT name, quantity from products")#sp.product_name, count(ss.product_id) as 'quantity' " +
						# "FROM smartcoolerstocks ss JOIN smartcoolerproducts sp " +
						# "ON sp.product_id = ss.product_id " +
						# "GROUP by sp.product_name")
	rows = cursor.fetchall()



	for row in rows:
		name, quantity = row
		drinksDict[name] = quantity


	# print(drinksDict)
	# print(drinksDict['Fanta Orange'])

	for x in rows:
		name, quantity = x
		if quantity == 2:
			drinksBelowSafeLevel[name] = quantity
		elif quantity > 2:
			drinksWithinSafeLevel[name] = quantity

	connection.close()

	# print('\n')
	# print(drinksBelowSafeLevel)
	# print('\n')
	# print(drinksWithinSafeLevel)


# https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
def merge_two_dicts(x, y):
	z = x.copy()   # start with x's keys and values
	z.update(y)	# modifies z with y's keys and values & returns None
	return z





count_BSL = 0
count_WSL = 0


# Return current date time in YYYY-MM-DD HH:mm
def getCurrentDateTime():
	global currentDT
	now = datetime.datetime.now()
	currentDT = now.strftime("%Y-%m-%d %H:%M")



getCurrentDateTime()




# https://stackoverflow.com/questions/9014233/how-do-i-check-if-an-insert-was-successful-with-mysqldb-in-python
def connectDB_createNewConvoId():
	global convoId
	#Connect to azure db
	## Create new Convo id
	driver = 'ODBC Driver 17 for SQL Server'
	server = 'tcp:smartcooler3.database.windows.net,1433'
	database = 'smartcooler3'
	uid = 'acn_admin'
	pw = 'Accenture1'

	connection = pyodbc.connect('Driver=' + driver + ';Server=' + server + ';Database=' + database + ';' + 'Uid=' + uid + ';Pwd=' + pw)
	#connection = pymssql.connect(server=server, user=uid, password=pw, database=database)
	cursor = connection.cursor()
	cursor.execute("INSERT INTO Conversations VALUES ('" + currentDT + "')")
	cursor.execute("SELECT MAX(ConversationId) FROM Conversations")
	# rows = cursor.fetchall()

	# Check the newly created Convo id

	for row in cursor:
		# print(row[0])
		convoId = row[0]

	connection.commit()
	# logging.warn("%d", affected_count)


	connection.close()




def connectDB_InsertRestockDrinks(orderJson):

	#Connect to azure db
	## Create new Convo id
	driver = 'ODBC Driver 17 for SQL Server'
	server = 'tcp:smartcooler3.database.windows.net,1433'
	database = 'smartcooler3'
	uid = 'acn_admin'
	pw = 'Accenture1'

	connection = pyodbc.connect('Driver=' + driver + ';Server=' + server + ';Database=' + database + ';' + 'Uid=' + uid + ';Pwd=' + pw)
	#connection = pymssql.connect(server=server, user=uid, password=pw, database=database)
	cursor = connection.cursor()


	orderJson = ast.literal_eval(json.dumps(orderJson))


	for key, value in orderJson.items():

		print(key, value)

		if (value != 0):
			query_str = "INSERT INTO Drinks VALUES ('" + key + "', " + str(value) + ", 'No', " + str(convoId) + ")";
			cursor.execute(query_str)


	# for row in cursor:
	# 	print(row)


	connection.commit()



	connection.close()




connectDB_createNewConvoId()

time.sleep(2)

# connectDB_InsertRestockDrinks(mergeDict)


# ###################### Steven function
# def startSmartCooler():
def askDrinksBelowSafeLevel():
	global drinksBelowSafeLevel
	global drinksWithinSafeLevel
	# Connect to DB
	# End of DB Connection

	# Once DB Connection results are stored, let Bot start talking

	# totalItems = { "Coke": "1", "Dasani": "5", "Sprite": "10"}

	totalItems = drinksBelowSafeLevel


	for obj in totalItems.keys():
		stop_listening()
		# Bot starts asking for each drink to be restocked
		voice.speak_text(obj + " has a quantity of " + totalItems[obj] + ", how many would you like to restock?")
		print( obj + " has a quantity of 1, how many would you like to restock?")
		start_listening()
		searching = True
		while searching:
			recordings = os.listdir("data")
			for recording in recordings:

				if ".wav" in recording:

					if recording == "output.wav":
						pass
					else:
						print("Analyzing: " + recording)
						client.run("data/" + recording)

						try:
							os.remove( "data/" +  recording)
							# pass
						except:
							pass

						# print(client.last_request)

						if client.last_request is None or len(client.last_request) < 1:

							pass
						else:


							analysis = text_analysis.analyze_text(client.last_request)
							print(analysis.entities)
							number = text_analysis.find_entity_key(analysis.entities, "builtin.number")
							print(number)
							if number == "Not found" or number is None:
								stop_listening()
								voice.speak_text("Please provide a number");
								pass

							else:
								searching = False
								break

		# Run askDrinksWithinSafeLevel() to continue asking the remaining drinks
		# askDrinksWithinSafeLevel()


def askDrinksWithinSafeLevel():
	global drinksBelowSafeLevel
	global drinksWithinSafeLevel
	totalItems = drinksWithinSafeLevel


	for obj in totalItems.keys():
		stop_listening()
		# Bot starts asking for each drink to be restocked
		voice.speak_text(obj + " has a quantity of " + totalItems[obj] + ", how many would you like to restock?")
		print( obj + " has a quantity of 1, how many would you like to restock?")
		start_listening()
		searching = True
		while searching:
			recordings = os.listdir("data")
			for recording in recordings:

				if ".wav" in recording:

					if recording == "output.wav":
						pass
					else:
						print("Analyzing: " + recording)
						client.run("data/" + recording)

						try:
							os.remove( "data/" +  recording)
							# pass
						except:
							pass

						# print(client.last_request)

						if client.last_request is None or len(client.last_request) < 1:

							pass
						else:


							analysis = text_analysis.analyze_text(client.last_request)
							print(analysis.entities)
							number = text_analysis.find_entity_key(analysis.entities, "builtin.number")
							print(number)
							if number == "Not found" or number is None:
								stop_listening()
								voice.speak_text("Please provide a number");
								pass

							else:
								searching = False
								break


def FetchDrinks():
	global drinksBelowSafeLevel
	global drinksWithinSafeLevel
	connectDB_retrieveDrinks()


	# print("BSL: " + str(drinksBelowSafeLevel))
	# print("WSL: " + str(drinksWithinSafeLevel))

	mergeDict = merge_two_dicts(drinksBelowSafeLevel, drinksWithinSafeLevel)
	return mergeDict

# FetchDrinks()
