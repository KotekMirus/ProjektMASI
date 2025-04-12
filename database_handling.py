import datetime
import json
import os

def check_database_existence():
    if not os.path.isfile('database.json'):
        with open('database.json','w') as file:
            json.dump({},file,indent = 3)

def save_entry(symbols,position):
    check_database_existence()
    database = None
    with open('database.json','r') as file:
        database = json.load(file)
    key = str(datetime.datetime.now())
    database[key] = {'symbol1':symbols[0],'symbol2':symbols[1],'symbol3':symbols[2],'symbol4':symbols[3],'position':position}
    with open('database.json','w') as file:
        json.dump(database,file,indent = 3)