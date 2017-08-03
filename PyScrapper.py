from pymongo import MongoClient
from lxml import html
import requests
from datetime import datetime

client = MongoClient()
db = client.test

xpathNew		= '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div[2]/text()'
xpathUsed		= '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[2]/text()'
xpathPreRelease = '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[2]/text()'

dbGames = db.games5
dbGamesHistory = db.gamesHistory5

games = dbGames.find()
for game in games:
	dbTitle		= game["GameTitle"]
	dbURL		= game["EBGamesURL"]

	page 		= requests.get(dbURL)
	tree 		= html.fromstring(page.content)
	prePrice	= tree.xpath(xpathPreRelease)

	if prePrice == []:
		#game is released, look for new\used prices
		if "NewPrice" in game:
			dbNewPrice	= game["NewPrice"]
		else:
			dbNewPrice = 0

		if "UsedPrice" in game:
			dbUsedPrice	= game["UsedPrice"]
		else:
			dbUsedPrice = 0
		
		newPrice = tree.xpath(xpathNew)
		usedPrice = tree.xpath(xpathUsed)
		
		if dbNewPrice == 0 or dbUsedPrice == 0 or newPrice < dbNewPrice or usedPrice < dbUsedPrice:
			#dbGamesHistory.insert(dbGames.find({"GameURL":dbURL}))
			dbGames.update_one(
				{"GameTitle": dbTitle},
				{
					"$set": {
						"NewPrice"	: newPrice,
						"UsedPrice"	: usedPrice,
					}
				}
			)
			print(game["GameTitle"], "changed")
		
	else:
		#game is pre-release, priced as in prePrice
		if "PrePrice" in game:
			dbPrePrice	= game["PrePrice"]
		else:
			dbPrePrice	= 0
			#prePrice
		
		if dbPrePrice == 0 or prePrice < dbPrePrice:
			#dbGamesHistory.insert(dbGames.find({"GameURL":dbURL}))
			dbGames.update_one(
				{"GameTitle": dbTitle},
				{
					"$set": {
						"PreReleasePrice"	: prePrice,
					}
				}
			)
			print(game["GameTitle"], "changed")