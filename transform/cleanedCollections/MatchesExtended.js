db.matches.find({})
db.matches.aggregate([
{
	$lookup: {
	     from: "teams",
         localField: "TeamHomeID",
         foreignField: "TeamID",
         as: "TeamHome"}
	},
	{$unwind: "$TeamHome"},
	{
		$lookup: {
	     from: "teams",
         localField: "TeamAwayID",
         foreignField: "TeamID",
         as: "TeamAway"}
	},
	{$unwind: "$TeamAway"},
	{$project: {"TeamHome._id": 0, "TeamAway._id": 0,  "TeamHomeID" : 0, "TeamAwayID": 0}},
	{$out: "matchesExtended"}

])

db.matchesExtended.update({},{
	$rename:{
		"TeamHomeFormation" : "TeamHome.TeamHomeFormation",
		"TeamAwayFormation" : "TeamAway.TeamAwayFormation",
		"ResultOfTeamHome" : "TeamHome.ResultOfTeamHome"
	}
} 
,{multi:true}
)
db.matchesExtended.find({})

      
      