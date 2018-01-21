import argparse
import logging
import time
import sys, os
import json
from pymongo import MongoClient # Library mongo driver
import pprint # getting documents in mongodb


#================================================================
                        #LOGGER SETTINGS
#================================================================
logger = logging.getLogger('classify_images.py')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)

#================================================================
                        #MENU SETTINGS
#================================================================

def print_menu():
    print (30 * "-", "MENU", 30 * "-")
    print("1. USER VIEW")
    print("2. ANALYST VIEW")
    print("3. ADMINISTRATOR VIEW")
    print("4. Quitter")
    print(67 * "-")

def print_sub_menu_1():
    print (30 * "-", "MENU", 30 * "-")
    print("1. Afficher le nombre de but par joueur")
    print("2. Afficher le nombre de cleansheet par gardien")
    print("3. Afficher V/N/D par équipe sur les n derniers match")
    print("4. Afficher le nombre de pénalty concédé par joueur")
    print("5. Retour")
    print(67 * "-")

def print_sub_menu_2():
    print (30 * "-", "MENU", 30 * "-")
    print("1. Afficher le top n joueurs")
    print("2. Afficher le top n équipe de la premier league")
    print("3. Afficher la comparaison entre l'équipe X et les autres équipe du top n")
    print("4. Retour")
    print(67 * "-")

def print_sub_menu_3():  ## Your menu design here
    print (30 * "-", "MENU", 30 * "-")
    print("1. Menu Option 1")
    print("2. Menu Option 2")
    print("5. Retour")
    print(67 * "-")

#================================================================
                        #QUERIES
#================================================================
def Simple_query():
    #Query find One document
    #For example this find the first document that contain a victory for a the home team
    print(30 * "-", "FIND ONE DOCUMENTS", 30 * "-")
    pprint.pprint(collectionMatch.find_one({'TeamHome.ResultOfTeamHome': '1'}))

def Multiple_doc_query():
    #Query find multiple documents:
    print(30 * "-", "FIND MULTIPLE DOCUMENTS", 30 * "-")
    for doc in collectionMatch.find({'TeamHome.ResultOfTeamHome': '1'}):
        pprint.pprint(doc)

#================================================================
                        #MAIN
#================================================================
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
collectionMatch = db['matchesExtended']
collectionAction = db['actionsExtended']
logger.info("got the collections")

#2 loops because menu depth = 2
loop = True
loop1 = True
#Displaying
while loop:  ## While loop which will keep going until loop = False
    print_menu()  ## Displays menu
    choice = int(input("Enter your choice [1-4]: "))

    if choice == 1:
        loop1 = True
        print("Menu 1 simple query")
        print_sub_menu_1()
        while loop1:
            choice2 = int(input("Enter your choice [1-5]: "))
            if choice2 == 1:
                print("Sub Menu 1.1")
                # TODO 1st user query here
                print_sub_menu_1()
            elif choice2 == 2:
                print("Menu 1.2 user")
                #TODO 2nd user query here
                print_sub_menu_1()
            elif choice2 == 3:
                print("Menu 1.3 user")
                # TODO 3rd user query here
                print_sub_menu_1()
            elif choice2 == 4:
                print("Menu 1.4 user")
                # TODO 4th user query here
                print_sub_menu_1()
            elif choice2 == 5:
                print("Menu 1.5 user")
                loop1 = False  # This will make the while loop to end as not value of loop is set to False
            else:
                # Any integer inputs other than values 1-5 we print an error message
                input("Wrong option selection. Enter any key to try again..")
    elif choice == 2:
        loop1 = True
        print("Menu 2 multiple queries")
        print_sub_menu_2()
        while loop1:
            choice2 = int(input("Enter your choice [1-4]: "))
            if choice2 == 1:
                print("Sub Menu 1.1 analyst")
                # TODO 1st analyst query here
                print_sub_menu_2()
            elif choice2 == 2:
                print("Menu 1.2 analyst")
                #TODO 2nd user query here
                print_sub_menu_2()
            elif choice2 == 3:
                print("Menu 1.3 analyst")
                # TODO 3rd user query here
                print_sub_menu_2()
            elif choice2 == 4:
                print("Menu 1.4 analyst")
                loop1 = False  # This will make the while loop to end as not value of loop is set to False
            else:
                # Any integer inputs other than values 1-5 we print an error message
                input("Wrong option selection. Enter any key to try again..")
    elif choice == 3:
        loop1 = True
        print("Menu 3 has been selected")
        print_sub_menu_3()
        while loop1:
            choice2 = int(input("Enter your choice [1-3]: "))
            if choice2 == 1:
                print("Sub Menu 3.1 ADMIN")
                # TODO 1st admin query here
            elif choice2 == 2:
                print("Menu 3.2 ADMIN")
                # TODO 2nd admin query here
            elif choice2 == 3:
                print("Menu 1.5 ADMIN")
                loop1 = False  # This will make the while loop to end as not value of loop is set to False
            else:
                # Any integer inputs other than values 1-5 we print an error message
                input("Wrong option selection. Enter any key to try again..")
    elif choice == 4:
        print("Menu 4 has been selected")
        loop = False  # This will make the while loop to end as not value of loop is set to False
    else:
        # Any integer inputs other than values 1-5 we print an error message
        input("Wrong option selection. Enter any key to try again..")