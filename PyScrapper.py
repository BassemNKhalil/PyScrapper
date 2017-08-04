from pymongo import MongoClient
from lxml import html
import requests
from datetime import datetime

client = MongoClient()
db = client.test

xpathNew		= '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div[2]/text()'
xpathUsed		= '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[2]/text()'
xpathPreRelease = '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[2]/text()'

dbGames = db.games6
dbGamesHistory = db.gamesHistory6

games = dbGames.find()
for game in games:
	insertIntoHistory = False
	dbTitle		= game["GameTitle"]
	dbURL		= game["EBGamesURL"]

	page 		= requests.get(dbURL)
	tree 		= html.fromstring(page.content)
	prePrice	= tree.xpath(xpathPreRelease)
	
	if prePrice == []:
		#game is released
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
		
		if (len(newPrice) > 0 and (dbNewPrice == 0 or float((newPrice[0][1:]) < dbNewPrice))):
			insertIntoHistory = True
			#if (dbNewPrice == 0)
			dbGames.update_one(
				{"GameTitle": dbTitle},
				{
					"$set": {
						"NewPrice"	: float((newPrice[0][1:]))
					}
				}
			)
			print(game["GameTitle"], "changed-new")
		
		if (len(usedPrice) > 0 and (dbUsedPrice == 0 or float((usedPrice[0][1:]) < dbUsedPrice))):
			insertIntoHistory = True
			#dbGamesHistory.insert(dbGames.find({"GameURL":dbURL}))
			dbGames.update_one(
				{"GameTitle": dbTitle},
				{
					"$set": {
						"UsedPrice"	: float((usedPrice[0][1:]))
					}
				}
			)
			print(game["GameTitle"], "changed-used")

			
	else:
		#game is pre-release, priced as in prePrice
		if "PrePrice" in game:
			dbPrePrice	= game["PrePrice"]
		else:
			dbPrePrice	= 0
			#prePrice
		
		if (len(prePrice) > 0 and (dbPrePrice == 0 or float((prePrice[0][1:]) < dbPrePrice))):
			insertIntoHistory = True
			#dbGamesHistory.insert(dbGames.find({"GameURL":dbURL}))
			dbGames.update_one(
				{"GameTitle": dbTitle},
				{
					"$set": {
						"PreReleasePrice"	: float(prePrice[0][1:])
					}
				}
			)
			print(game["GameTitle"], "changed-pre")

	if insertIntoHistory:
		dbGamesHistory.insert(game)