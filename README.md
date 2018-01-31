# MPGalafaLeague
MPGalafaleague is a Console Application that gives you some statistics about Football Premier League in 2011/2012 season.

# Installation

Requirements : 
- You must have a Mongo daemon running.

## 1. Retrieve Data with SQL format and transform it to CSV.

Run the R code in *transform/1_SQLtoCSV.R*

If you can't, you have the result in the directory transform/CSV.

## 2. Transform CSV to "plate" Json

Run the Python file *transform/2_CSVtoMongo.py*

This will install 4 collections in your Mongo installation.

## 3. Aggregate json to get 2 collections.

Run both JS scripts called *3_MatchesExtended.js* and *3_ActionsExtended.js*, which are located in *transform* folder.

You can run this on Studio 3T or in the console.

This will create 2 new collections called MatchesExtended and ActionsExtended.

## 4. Adjust some type attributes
All of the data is in string type. In order to handle queries with quantitative values, we must set some of the types from string to int.

For this, you will need to run *Query_to_execute.js* file.



Your database is now ready ! 

To launch the app, run the *CloudAppMongo.exe* file in *build\exe.win-amd64-3.6* folder.

Here you go ! 


# Contributors
Salem Ben Mabrouk

Badre-Addine FOUAD

Félicien Gazon

