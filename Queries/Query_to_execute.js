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