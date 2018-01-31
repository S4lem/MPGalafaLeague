# coding: utf-8
from pymongo import MongoClient
import logging
from tqdm import tqdm

# Setup logging
logger = logging.getLogger('transformCSVtoMongo.py')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)

def parseCSVToMongo(fromPath, mongo_ip, mongo_port, mongo_db, mongo_collection):
    #Connect to the db
    client = MongoClient(mongo_ip, mongo_port)
    db = client[mongo_db]
    collection = db[mongo_collection]

    #Read CSV
    try:
        f = open(fromPath,  encoding="utf8")
    except:
        return

    jsonLine = {}

    #Save column names
    names = cleanString(f.readline(), True, True).split(';')

    #Foreach line, Send single json to Mongodb
    for line in tqdm(f):
        lineSplitted = line.split(';')
        for index, column in enumerate(lineSplitted):
            jsonLine[names[index]] = cleanString(lineSplitted[index], True, True)

        collection.insert_one(jsonLine)
        jsonLine.clear()

    logger.info("Done for " + collection.name)

def cleanString(text, cleanQuotes = True, cleanLineBreak = True):
    if(cleanQuotes):
        newText = text.replace("'", "")
        newText = newText.replace('"', "")

    if(cleanLineBreak):
        newText = newText.replace("\n", "")

    return newText

parseCSVToMongo("CSV/Teams.csv","localhost",27017,"premierleague","teams")
parseCSVToMongo("CSV/Actions.csv","localhost",27017,"premierleague","actions")
parseCSVToMongo("CSV/Players.csv","localhost",27017,"premierleague","players")
parseCSVToMongo("CSV/Matches.csv","localhost",27017,"premierleague","matches")

