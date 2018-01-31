use premierleague;
//TEST DB
db.actionsExtended.find().pretty();
db.matchesExtended.find({"TeamHome.ResultOfTeamHome": {$exists: true}}).pretty();

//CONVERSION STRING TO INT
db.actionsExtended.find({"SummaryMatch.goals": {$exists: true}}).forEach(function(obj){ 
    obj.SummaryMatch.goals = new NumberInt(obj.SummaryMatch.goals);
    db.actionsExtended.save(obj);
});
db.actionsExtended.find({"CleanSheets": {$exists: true}}).forEach(function(obj){ 
    obj.CleanSheets = new NumberInt(obj.CleanSheets);
    db.actionsExtended.save(obj);
});
db.actionsExtended.find({"PenaltiesConceded": {$exists: true}}).forEach(function(obj){ 
    obj.PenaltiesConceded = new NumberInt(obj.PenaltiesConceded);
    db.actionsExtended.save(obj);
});
db.actionsExtended.find({"GoalsConceded": {$exists: true}}).forEach(function(obj){ 
    obj.GoalsConceded = new NumberInt(obj.GoalsConceded);
    db.actionsExtended.save(obj);
});

db.matchesExtended.find({"TeamHome.ResultOfTeamHome": {$exists: true}}).forEach(function(obj){ 
    obj.TeamHome.ResultOfTeamHome = new NumberInt(obj.TeamHome.ResultOfTeamHome);
    db.matchesExtended.save(obj);
});
//--------------------------------------------------------------------------------------------------------

//nombre de but total inscrit par joueur durant le championnat
db.actionsExtended.aggregate([
{$group:{_id:"$Player.Name", "totalGoals":{$sum:"$SummaryMatch.goals"}}}
]).toArray()

//nombre de but par joueur ordre decroissant
db.actionsExtended.aggregate([
{$group:{_id:"$Player.Name", "totalGoals":{$sum:"$SummaryMatch.goals"}}},
{$sort:{'totalGoals':-1}},
])

//5 meilleurs butteurs ordre decroissant
db.actionsExtended.aggregate([
{$group:{_id:"$Player.Name", "totalGoals":{$sum:"$SummaryMatch.goals"}}},
{$sort:{'totalGoals':-1}},
{ $limit : 5 }
])

//Position id des gardiens de but 
db.actionsExtended.find({"CleanSheets":{$ne:"0"},"SummaryMatch.PositionID" : "1"},
{"Player.Name":1,"SummaryMatch.PositionID" : 1,"CleanSheets":1}).pretty();

//5 meilleur gardien
db.actionsExtended.aggregate([
{$match:{"SummaryMatch.PositionID" : "1"}},
{$group:{_id:"$Player.Name", "totalCleansheet":{$sum:"$CleanSheets"}}},
{$sort:{'totalCleansheet':-1}},
{ $limit : 5 }
])

//penalty concedé par joueur
db.actionsExtended.aggregate([
{$group:{_id:"$Player.Name", "PenaltiesConceded":{$sum:"$PenaltiesConceded"}}},
{$sort:{'PenaltiesConceded':-1}},
{ $limit : 5 }
])

//but concedé par joueur
db.actionsExtended.aggregate([
{$group:{_id:"$Player.Name", "GoalsConceded":{$sum:"$GoalsConceded"}}},
{$sort:{'GoalsConceded':-1}},
{ $limit : 5 }
])


//classement top n teams
db.matchesExtended.aggregate([
{$group:{_id:"$TeamHome.Name", 
"classement":{$sum:"$TeamHome.ResultOfTeamHome"}}},
{$sort:{'classement':-1}}
])

//nb victoire par equipe
db.matchesExtended.aggregate([
{$match:{"TeamHome.ResultOfTeamHome" : 1}},
{$group:{_id:"$TeamHome.Name", "victoires":{$sum:1}}},
{$sort:{'victoires':-1}}])
//nb defaite par equipe
db.matchesExtended.aggregate([
{$match:{"TeamHome.ResultOfTeamHome" : -1}},
{$group:{_id:"$TeamHome.Name", "defaites":{$sum:1}}},
{$sort:{'defaites':-1}}])
//nb nul par equipe
db.matchesExtended.aggregate([
{$match:{"TeamHome.ResultOfTeamHome" : 0}},
{$group:{_id:"$TeamHome.Name", "nul":{$sum:1}}},
{$sort:{'nul':-1}}])
// get the score of a specific team
db.matchesExtended.aggregate([
{$match:{"TeamHome.Name" :{ $regex: /Man/ }}},
{$group:{_id:"$TeamHome.Name", 
"Score":{$sum:"$TeamHome.ResultOfTeamHome"}}},
{$sort:{'Score':-1}}
])
//get all teams 
db.matchesExtended.distinct("TeamHome.Name")
//Admin view
