from pymongo import MongoClient
from lxml import html
import requests
from datetime import datetime

client = MongoClient()
db = client.test

xpathNew		= '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div[2]/text()'
xpathUsed		= '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[2]/text()'
xpathPreRelease = '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[2]/text()'

dbGames = db.games
dbGamesHistory = db.gamesHistory

diff = 0+1
print()
print("diff:", diff)
print()

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
		
		if len(newPrice) > 0:
			floatNewPrice = float((newPrice[0][1:]))-diff
			if dbNewPrice == 0 or floatNewPrice < dbNewPrice:
				insertIntoHistory = True
				dbGames.update_one(
					{"GameTitle": dbTitle},
					{
						"$set": {
							"NewPrice" : floatNewPrice
						}
					}
				)
				print(game["GameTitle"], "changed-new")
			else:
				print(game["GameTitle"], "notchanged-new")

		if len(usedPrice) > 0:
			floatUsedPrice = float((usedPrice[0][1:]))-diff
			if dbUsedPrice == 0 or floatUsedPrice < dbUsedPrice:
				insertIntoHistory = True
				dbGames.update_one(
					{"GameTitle": dbTitle},
					{
						"$set": {
							"UsedPrice"	: floatUsedPrice
						}
					}
				)
				print(game["GameTitle"], "changed-used")
			else:
				print(game["GameTitle"], "notchanged-used")
	else:
		#game is pre-release, priced as in prePrice
		if "PrePrice" in game:
			dbPrePrice	= game["PrePrice"]
		else:
			dbPrePrice	= 0
			#prePrice
		
		if len(prePrice) > 0:
			floatPrePrice = float((prePrice[0][1:]))-diff
			if dbPrePrice == 0 or floatPrePrice < dbPrePrice:
				insertIntoHistory = True
				dbGames.update_one(
					{"GameTitle": dbTitle},
					{
						"$set": {
							"PrePrice" : floatPrePrice
						}
					}
				)
				print(game["GameTitle"], "changed-pre")
			else:
				print(game["GameTitle"], "notchanged-pre")

	if insertIntoHistory:
		result = dbGamesHistory.insert_one(
			{
				"GameTitle": game["GameTitle"],
				"EBGamesURL": game["EBGamesURL"],
			}
		)

		if "NewPrice" in game:
			dbGamesHistory.update_one(
				{"_id": result.inserted_id},
				{
					"$set": {
						"NewPrice" : floatNewPrice
					}
				}
			)		
		if "UsedPrice" in game:
			dbGamesHistory.update_one(
				{"_id": result.inserted_id},
				{
					"$set": {
						"UsedPrice" : floatUsedPrice
					}
				}
			)
		if "PrePrice" in game:
			dbGamesHistory.update_one(
				{"_id": result.inserted_id},
				{
					"$set": {
						"PrePrice" : floatPrePrice
					}
				}
			)