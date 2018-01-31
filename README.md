# MPGalafaLeague
MPGalafaleague est une application informant les utilisateurs des statistiques de la Premier League anglaise saison 2015-2016.

# Objectif du projet MPGalafaLeague: 
Outil complémentaire à l'application MonPetitGazon --> Permettant aux joueurs de composer la meilleure équipe possible en premierLeague
                                                   --> Permettant aux joueurs de réaliser le meilleur Mercato possible
                                                   -->
Facilité l'accés aux statistiques footballistiques anglaise

# Installations
TODO: Salem
Installation de la base de donnée
1/CSV to json 
2/query_to_execute.js 

# MPGalafaLeague

# Objectif du projet MPGalafaLeague: 

# Installation

Requirements : 
You must have a Mondo daemon running.

1. Retrieve Data with SQL format and transform it to CSV.

Run the R code in transform/1_SQLtoCSV.R
If you can't, you have the result in the directory transform/CSV.

2. Transform CSV to "plate" Json

Run the Python file transform/2_CSVtoMongo.py
This will install 4 collections in your Mongo installation.

3. Aggregate json to get 2 collections.

Run both JS scripts called 3_MatchesExtended.js and 3_ActionsExtended.js, in transform folder.
You can run this on Studio 3T or in the console.

This will create 2 new collections called MatchesExtended and ActionsExtended.

4. Adjust some type attibute
All of the data is in string type. 
In order to handle queries with quantitative values, we must set some of the types from string to int.

For this, you will need to run Query_to_execute.js file.

Your database is now ready ! 

To launch the app, run the CloudAppMongo.exe file in build\exe.win-amd64-3.6 folder.

Here you go ! 


# Liste des contributeurs
Salem Ben Mabrouk

Badre-Addine FOUAD

Félicien Gazon

