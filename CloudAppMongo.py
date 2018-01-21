import argparse
import logging
import time
import sys, os
import json
from pymongo import MongoClient # Library mongo driver
import pprint # getting documents in mongodb



# Setup logging
logger = logging.getLogger('classify_images.py')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)

## Text menu in Python

def print_menu():  ## Your menu design here
    print (30 * "-", "MENU", 30 * "-")
    print("1. Menu Option 1")
    print("2. Menu Option 2")
    print("3. Menu Option 3")
    print("4. Menu Option 4")
    print("5. Exit")
    print(67 * "-")

def setting_mongo():
    #Connect to mongoClient
    client = MongoClient() # Connect to the default host and port
    logger.info("connected")
    if not client:
        client = MongoClient('localhost', 27017)
        logger.info("connected")
    #Getting the database
    db = client.premierleague
    logger.info("got the DB")
    #Getting the collection
    d = dict((db, [collection for collection in client[db].collection_names(include_system_collections=False)])
             for db in client.database_names())
    print(30 * "-", "DISPLAY COLLECTIONS", 30 * "-")
    pprint.pprint(json.dumps(d))
    collection = db['matchesExtended']
    logger.info("got the collections")
    #Query find One document
    #For example this find the first document that contain a victory for a the home team
    print(30 * "-", "FIND ONE DOCUMENTS", 30 * "-")
    pprint.pprint(collection.find_one({'TeamHome.ResultOfTeamHome': '1'}))
    print(30 * "-", "FIND MULTIPLE DOCUMENTS", 30 * "-")

    #Query find multiple documents:
    for doc in collection.find({'TeamHome.ResultOfTeamHome': '1'}):
        pprint.pprint(doc)




setting_mongo()
#MAIN
loop = True
while loop:  ## While loop which will keep going until loop = False
    print_menu()  ## Displays menu
    choice = int(input("Enter your choice [1-5]: "))

    if choice == 1:
        print("Menu 1 has been selected")
        ## You can add your code or functions here
    elif choice == 2:
        print("Menu 2 has been selected")
        ## You can add your code or functions here
    elif choice == 3:
        print("Menu 3 has been selected")

        ## You can add your code or functions here
    elif choice == 4:
        print("Menu 4 has been selected")

        ## You can add your code or functions here
    elif choice == 5:
        print("Menu 5 has been selected")

        ## You can add your code or functions here
        loop = False  # This will make the while loop to end as not value of loop is set to False
    else:
        # Any integer inputs other than values 1-5 we print an error message
        input("Wrong option selection. Enter any key to try again..")
