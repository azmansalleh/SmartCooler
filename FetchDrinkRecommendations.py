# from bs4 import BeautifulSoup
# import random
# import requests

# from inspect import getsourcefile
# import os.path
# import sys
#import pymssql
import pyodbc


# current_path = os.path.abspath(getsourcefile(lambda:0))
# current_dir = os.path.dirname(current_path)
# parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

# sys.path.insert(0, parent_dir)

# from LanguageProcess import text_analysis

def FetchDrinkRecommendations():
    # quote_type = text_analysis.find_entity_key(entities, "quote_type")

    driver = 'ODBC Driver 17 for SQL Server'
    server = 'tcp:smartcooler2.database.windows.net,1433'
    database = 'smartcooler2'
    uid = 'acn_admin'
    pw = 'Accenture1'
    conn = pyodbc.connect('Driver=' + driver + ';Server=' + server + ';Database=' + database + ';' + 
		'Uid=' + uid + ';Pwd=' + pw)


    # connection = pymssql.connect(server=server, user=uid, password=pw, database=database)
	
    cursor = conn.cursor()
    cursor.execute('SELECT TOP 1 name, COUNT(name) AS MOST_FREQUENT FROM drinks GROUP BY name ORDER BY COUNT(name) DESC')

    rows = cursor.fetchall()

    for row in rows:
    	name, quantity = row
    	recommendedDrink = name


    conn.close()

    print(recommendedDrink)

FetchDrinkRecommendations()


def FetchLastRestockCount(drink):
	
	
    # quote_type = text_analysis.find_entity_key(entities, "quote_type")

    driver = 'ODBC Driver 17 for SQL Server'
    server = 'tcp:smartcooler2.database.windows.net,1433'
    database = 'smartcooler2'
    uid = 'acn_admin'
    pw = 'Accenture1'
    conn = pyodbc.connect('Driver=' + driver + ';Server=' + server + ';Database=' + database + ';' + 
		'Uid=' + uid + ';Pwd=' + pw)


    # connection = pymssql.connect(server=server, user=uid, password=pw, database=database)
	
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 name,quantity FROM drinks WHERE name = (SELECT MAX(name) FROM drinks WHERE name = '" +
    drink + "') ORDER BY drinkid DESC")

    rows = cursor.fetchall()

    check = False

    for row in rows:
    	check = True
    	name, quantity = row
    	lastRestockName = name
    	lastRestockQty = quantity
    	
    if check == False:
    		lastRestockName = drink
    		lastRestockQty = 0


    conn.close()

    print(lastRestockName)
    print(lastRestockQty)

FetchLastRestockCount('Dasani')

