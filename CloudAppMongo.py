import argparse
import logging
import time
import sys, os
import json
import re
from bson.son import SON
from bson.code import Code
from pymongo import MongoClient  # Library mongo driver
import pprint  # getting documents in mongodb

# ================================================================
# LOGGER SETTINGS
# ================================================================
logger = logging.getLogger('classify_images.py')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)


# ================================================================
# MENU SETTINGS
# ================================================================

def print_menu():
    print(30 * "-", "MENU", 30 * "-")
    print("1. USER VIEW")
    print("2. ANALYST VIEW")
    print("3. ADMINISTRATOR VIEW")
    print("4. Quitter")
    print(67 * "-")


def print_sub_menu_1():
    print(30 * "-", "MENU", 30 * "-")
    print("1. Afficher le nombre de but par joueur")
    print("2. Afficher le nombre de cleansheet par gardien")
    print("3. Afficher le nombre de but concédé par joueur")
    print("4. Afficher le nombre de pénalty concédé par joueur")
    print("5. Retour")
    print(67 * "-")


def print_sub_menu_2():
    print(30 * "-", "MENU", 30 * "-")
    print("1. Afficher V/N/D par équipe sur les n derniers match")
    print("2. Afficher le top n équipe de la premier league")
    print("3. Afficher la comparaison entre l'équipe X et les autres équipe du top n")
    print("4. Retour")
    print(67 * "-")


def print_sub_menu_3():  ## UTILISER DES REQUETES AVEC EXPLAIN
    print(30 * "-", "MENU", 30 * "-")
    print("1. ADMIN Menu Option 1")
    print("2. ADMIN Menu Option 2")
    print("5. Retour")
    print(67 * "-")


# ================================================================
# QUERIES
# ================================================================

# TEST queries
def Simple_query():
    # Query find One document
    # For example this find the first document that contain a victory for a the home team
    print(30 * "-", "FIND ONE DOCUMENTS", 30 * "-")
    pprint.pprint(collectionMatch.find_one({'TeamHome.ResultOfTeamHome': '1'}))


def Multiple_doc_query():
    # Query find multiple documents:
    print(30 * "-", "FIND MULTIPLE DOCUMENTS", 30 * "-")
    for doc in collectionMatch.find({'TeamHome.ResultOfTeamHome': '1'}):
        pprint.pprint(doc)


# ================================================================
# USER QUERIES
# ================================================================

# Top 5 best goaler
def Nb_goal_per_player():
    pipeline = [
        {"$group": {"_id": "$Player.Name", "totalGoals": {"$sum": "$SummaryMatch.goals"}}},
        {"$sort": {"totalGoals": -1}},
        {"$limit": 5}
    ]
    print(30 * "-", "TOP 5 Player", 30 * "-")
    pprint.pprint(list(collectionAction.aggregate(pipeline)))


# 5 Best Goalkeepers
def Nb_cleansheet_per_player():  # Done
    pipeline = [
        {"$match": {"SummaryMatch.PositionID": "1"}},
        {"$group": {"_id": "$Player.Name", "Total Cleansheet": {"$sum": "$CleanSheets"}}},
        {"$sort": {"Total Cleansheet": -1}},
        {"$limit": 5}

    ]
    print(30 * "-", "TOP 5 Goalkeeper per CleanSheet", 30 * "-")
    pprint.pprint(list(collectionAction.aggregate(pipeline)))


# def Nb_goal_per_player():
#
#     print(30 * "-", "Player names", 30 * "-")
#
#     map =  Code("function () { emit(this.Player.Name, this.SummaryMatch.goals);}")
#
#     reduce =  Code("function (key, values) { return Array.sum(values);}")
#
#     result = db.actionsExtended.map_reduce(map, reduce, "myresults")
#
#     pprint.pprint(list(result.find()))

def Nb_GoalConceded_per_player():
    pipeline = [

        {"$group": {"_id": "$Player.Name", "GoalsConceded": {"$sum": "$GoalsConceded"}}},
        {"$sort": {"GoalsConceded": -1}},
        {"$limit": 5}
    ]
    print(30 * "-", "Goal conceded per player", 30 * "-")
    pprint.pprint(list(collectionAction.aggregate(pipeline)))


def Nb_penalty_conceded_per_player():
    pipeline = [

        {"$group": {"_id": "$Player.Name", "PenaltiesConceded": {"$sum": "$PenaltiesConceded"}}},
        {"$sort": {"PenaltiesConceded": -1}},
        {"$limit": 5}
    ]
    print(30 * "-", "TOP 5 Penalties conceded per player", 30 * "-")
    pprint.pprint(list(collectionAction.aggregate(pipeline)))


# ================================================================
# ANALYST QUERIES
# ================================================================
def Nb_Victories_per_Team():
    pipeline = [
        {"$match": {"TeamHome.ResultOfTeamHome": 1}},
        {"$group": {"_id": "$TeamHome.Name", "victoires": {"$sum": 1}}},
        {"$sort": {"victoires": -1}}
    ]
    print(30 * "-", "Victory per Team", 30 * "-")
    pprint.pprint(list(collectionMatch.aggregate(pipeline)))


def Nb_Defaite_per_Team():
    pipeline = [
        {"$match": {"TeamHome.ResultOfTeamHome": -1}},
        {"$group": {"_id": "$TeamHome.Name", "defaites": {"$sum": 1}}},
        {"$sort": {"defaites": -1}}
    ]
    print(30 * "-", "Defaite per Team", 30 * "-")
    pprint.pprint(list(collectionMatch.aggregate(pipeline)))


def Nb_Nul_per_Team():
    pipeline = [
        {"$match": {"TeamHome.ResultOfTeamHome": 0}},
        {"$group": {"_id": "$TeamHome.Name", "nul": {"$sum": 1}}},
        {"$sort": {"nul": -1}}
    ]
    print(30 * "-", "nul per Team", 30 * "-")
    pprint.pprint(list(collectionMatch.aggregate(pipeline)))


def Classment_teams_premierleague():
    pipeline = [
        {"$group": {"_id": "$TeamHome.Name", "Score:": {"$sum": "$TeamHome.ResultOfTeamHome"}}},
        {"$sort": {"Score:": -1}},
        {"$limit": 10}
    ]
    print(30 * "-", "Classment PremierLeague TOP 10", 30 * "-")
    pprint.pprint(list(collectionMatch.aggregate(pipeline)))


def print_teams():
    print(30 * "-", "List of premier league teams", 30 * "-")
    pprint.pprint(collectionMatch.distinct("TeamHome.Name"))


def score_specific_team(team):
    pipeline = [
        {"$match": {"TeamHome.Name": {"$regex": team, "$options": "i"}}},
        {"$group": {"_id": "$TeamHome.Name",
                    "Score": {"$sum": "$TeamHome.ResultOfTeamHome"}}},
        {"$sort": {'Score': -1}}
    ]
    print(30 * "-", "score of " + team, 30 * "-")
    pprint.pprint(list(collectionMatch.aggregate(pipeline)))


# ================================================================
# MAIN
# ================================================================

# Connect to mongoClient
client = MongoClient()  # Connect to the default host and port
logger.info("connected")
if not client:
    client = MongoClient('localhost', 27017)
    logger.info("connected")
# Getting the database
db = client.premierleague
logger.info("got the DB")
# Getting the collection
d = dict((db, [collection for collection in client[db].collection_names(include_system_collections=False)])
         for db in client.database_names())
#print(30 * "-", "DISPLAY COLLECTIONS", 30 * "-")
#pprint.pprint(json.dumps(d))
collectionMatch = db['matchesExtended']
collectionAction = db['actionsExtended']
logger.info("got the collections")

# 2 loops because menu depth = 2
loop = True
loop1 = True

# Displaying
while loop:  ## While loop which will keep going until loop = False
    print_menu()  ## Displays menu
    try:
        choice = int(input("Enter your choice [1-4]: "))
    except ValueError:
        choice = 0
    if choice == 1:
        loop1 = True
        print("Menu 1 simple query")
        print_sub_menu_1()
        while loop1:
            choice2 = int(input("Enter your choice [1-5]: "))
            if choice2 == 1:
                print("Sub Menu 1.1")
                Nb_goal_per_player()
                print_sub_menu_1()
            elif choice2 == 2:
                print("Menu 1.2 user")
                Nb_cleansheet_per_player()
                print_sub_menu_1()
            elif choice2 == 3:
                print("Menu 1.3 user")
                Nb_GoalConceded_per_player()
                print_sub_menu_1()
            elif choice2 == 4:
                print("Menu 1.4 user")
                # TODO 4th user query here
                Nb_penalty_conceded_per_player()
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
                Nb_Victories_per_Team()
                Nb_Nul_per_Team()
                Nb_Defaite_per_Team()
                print_sub_menu_2()
            elif choice2 == 2:
                print("Menu 1.2 analyst")
                # TODO 2nd user query here
                Classment_teams_premierleague()
                print_sub_menu_2()
            elif choice2 == 3:
                print("Menu 1.3 analyst")
                print_teams()
                team = input("Please input the team name to see the score...")
                # TODO 3rd user query here
                score_specific_team(team)
                print_sub_menu_2()
            elif choice2 == 4:
                print("Menu 1.4 analyst")
                loop1 = False
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
        loop = False
    else:
        # Any integer inputs other than values 1-4 we print an error message
        input("Wrong option selection. Enter any key to try again..")
