
db.actions.aggregate([
	{
	$lookup: {
	     from: "players",
         localField: "PlayerID",
         foreignField: "PlayerID",
         as: "Player"}
	},
	{$unwind: "$Player"},
	{$project: {"Player._id": 0}},
	
	{$lookup: {
	     from: "matches",
         localField: "MatchID",
         foreignField: "MatchID",
         as: "MatchDetails"}
	},
	 {$unwind: "$MatchDetails"},
	 
	{$lookup: {
	     from: "teams",
         localField: "MatchDetails.TeamAwayID",
         foreignField: "TeamID",
         as: "TeamAway"}
	},
	{$unwind: "$TeamAway"},
	
	{$lookup: {
	     from: "teams",
         localField: "MatchDetails.TeamHomeID",
         foreignField: "TeamID",
         as: "TeamHome"}
	},
	{$unwind: "$TeamHome"},
	//{$project: {"MatchDetails": 0, "TeamAgainst._id": 0}},

	//{$project: {"TeamID": 0, "Team1": 0, "Team2": 0, "PlayerID": 0 }},
	
	{$out: "actionsExtended"}

])

db.actionsExtended.find({}).forEach(
    function(doc) {
      doc.TeamAgainst = {}
      doc.TeamWith = {}
      doc.SummaryMatch = {}
      
      if(doc.TeamHome.TeamID == doc.TeamID){
		doc.TeamWith = doc.TeamHome
		doc.TeamAgainst = doc.TeamAway
		
       	doc.TeamWith["isHome"] = true
       	doc.TeamAgainst["isHome"] = false
       	
       	
       	if(doc.MatchDetails.ResultOfTeamHome == "1"){
       	  doc.SummaryMatch["MatchResult"] = "won"
       	}
       	else if (doc.MatchDetails.ResultOfTeamHome == "-1"){
       	  doc.SummaryMatch["MatchResult"] = "lost"
       	}
       	else if (doc.MatchDetails.ResultOfTeamHome == "-1"){
       	  doc.SummaryMatch["MatchResult"] = "draw"
       	}
       	else {
       	  doc.SummaryMatch["MatchResult"] = "unknown"
       	}
       	
      }
      else{
        doc.TeamWith = doc.TeamAway
        doc.TeamAgainst = doc.TeamHome
        
       	doc.TeamWith["isHome"] = false
       	doc.TeamAgainst["isHome"] = true
       	
       	if(doc.MatchDetails.ResultOfTeamHome == "1"){
       	  doc.SummaryMatch["MatchResult"] = "lost"
       	}
       	else if (doc.MatchDetails.ResultOfTeamHome == "-1"){
       	  doc.SummaryMatch["MatchResult"] = "won"
       	}
       	else if (doc.MatchDetails.ResultOfTeamHome == "-1"){
       	  doc.SummaryMatch["MatchResult"] = "draw"
       	}
       	else {
       	  doc.SummaryMatch["MatchResult"] = "unknown"
       	}
      }
//      doc.OtherData = {}
//      for(var field in doc){
//        if(field != ("TeamWith" && "TeamAgainst" && "Player" && "SummaryMatch" && "MatchID" && "_id" && "OtherData")){
//          doc.OtherData.field = field
//        }
//      }
      
      db.actionsExtended.save(doc)
   }
)


//Move fields to a new nested document.
db.actionsExtended.update({},{
	$rename:{
	  "Goals": "SummaryMatch.goals",
	  "TimePlayed":"SummaryMatch.TimePlayed",
	  "Assists":"SummaryMatch.Assists",
	  "YellowCards":"SummaryMatch.YellowCards",
	  "RedCards":"SummaryMatch.RedCards",
	  "passes_eff":"SummaryMatch.passes_eff",
	  "PositionID":"SummaryMatch.PositionID",
	  "TotalSuccessfulPassesAll":"SummaryMatch.TotalSuccessfulPassesAll",
	  "TotalUnsuccessfulPassesAll":"SummaryMatch.TotalUnsuccessfulPassesAll",
	}},{multi:true})

db.actionsExtended.aggregate([
	{$project: {"TeamID": 0, "Team1": 0, "Team2": 0, "PlayerID": 0 ,"MatchDetails": 0, "TeamHome": 0, "TeamAway": 0, "TeamAgainst._id": 0, "TeamWith._id": 0}},
	{$out: "actionsExtended"}
	
])

db.actionsExtended.find({})
