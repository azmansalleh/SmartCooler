from pydocumentdb import document_client
import json

class Query():
	def __init__(self):
		self.url = "https://lssmartcoolercosmosdb.documents.azure.com:443/"
		self.key = "SEtGPeFC6EPX568zHjLIgzUQnZmlaiQ2EvuP8JswQwy8CTGFEPHI91RFY0EAT8SwApZBhgxpv1SYRVEuqzYvkw=="
		self.dbID = "smartcooler"
		self.documentID = "cognitivedocuments"
		self.client = document_client.DocumentClient(self.url, {'masterKey': self.key})

		#Format DB
		self.dbQuery = "select * from r where r.id = '{0}'".format(self.dbID)
		self.db = list(self.client.QueryDatabases(self.dbQuery))[0]
		self.dbLink = self.db['_self']

		#Format documents
		self.docQuery = "select * from r where r.id = '{0}'".format(self.documentID)
		self.document = list(self.client.QueryCollections(self.dbLink, self.docQuery))[0]
		self.docLink = self.document['_self']

	def create(self,gender,age,smile,emotion,hair):
		self.client.CreateDocument((self.docLink),
		    { 
		        'Gender': gender,
		        'Age': age,
		        'Smile': smile,
		        'Emotions' : emotion,
		        'Hair' : hair


		    })

	def read(self):
		#Convert COSMOS dict type into readable JSON
		self.docs = self.client.ReadDocuments(self.docLink)
		self.output = (list(self.docs))
		self.jsonOutput = json.dumps(self.output)
		self.parsed = json.loads(self.jsonOutput)

		#Write to json file
		self.fp = open('demographic.json', 'a')
		self.fp.write(json.dumps(self.parsed, indent=4, sort_keys=True))

		# close the connection
		self.fp.close()


temp = Query()
temp.read()
