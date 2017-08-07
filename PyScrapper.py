from pymongo import MongoClient
from lxml import html
import requests
from datetime import datetime

client = MongoClient()
db = client.test

xpathFirstPrice = '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div[2]/text()'
xpathFirstCheck = '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div[1]/strong/text()'
xpathSecondPrice = '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[2]/text()'
#xpathSecondCheck = '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[1]/strong/text()'
xpathPreRelease = '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[2]/text()'

dbGames = db.games
dbGamesHistory = db.gamesHistory

diff = 7 #applies to %y only
diff2 = 4 #base diff
print()
print("diff:", diff)
print("diff2:", diff2)
print()

games = dbGames.find()
x=0
y=10
for game in games:
	insertIntoHistory = False
	dbTitle = game["GameTitle"]
	dbURL = game["EBGamesURL"]
	
	page = requests.get(dbURL)
	tree = html.fromstring(page.content)
	prePrice = tree.xpath(xpathPreRelease)
	
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
		
		firstCheck = tree.xpath(xpathFirstCheck)[0]
		#print("URL Type:", firstCheck)
		#secondCheck = tree.xpath(xpathSecondCheck)
		
		newPrice = 0
		usedPrice = 0
		if firstCheck == 'NEW':
			newPrice = tree.xpath(xpathFirstPrice)
			usedPrice = tree.xpath(xpathSecondPrice)
		elif firstCheck == 'PREOWNED':
			usedPrice = tree.xpath(xpathFirstPrice)
			newPrice = tree.xpath(xpathSecondPrice)
		
		if len(newPrice) > 0:
			if x%y==0:
				floatNewPrice = float((newPrice[0][1:]))-diff
			else:
				floatNewPrice = float((newPrice[0][1:]))-diff2
			
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
			#else:
				#print(game["GameTitle"], "notchanged-new")

		if len(usedPrice) > 0:
			if x%y==0:
				floatUsedPrice = float((usedPrice[0][1:]))-diff
			else:
				floatUsedPrice = float((usedPrice[0][1:]))-diff2
			
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
			#else:
				#print(game["GameTitle"], "notchanged-used")
	else:
		#game is pre-release, priced as in prePrice
		if "PrePrice" in game:
			dbPrePrice	= game["PrePrice"]
		else:
			dbPrePrice	= 0
			#prePrice
		
		if len(prePrice) > 0:
			if x%y==0:
				floatPrePrice = float((prePrice[0][1:]))-diff
			else:
				floatPrePrice = float((prePrice[0][1:]))-diff2
			
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
			#else:
				#print(game["GameTitle"], "notchanged-pre")

	latestGame = db.games.find_one({"GameTitle":game["GameTitle"]})
	if insertIntoHistory:
		result = dbGamesHistory.insert_one(
			{
				"GameTitle": game["GameTitle"],
				"EBGamesURL": game["EBGamesURL"],
			}
		)

		if "NewPrice" in latestGame:
			dbGamesHistory.update_one(
				{"_id": result.inserted_id},
				{
					"$set": {
						"NewPrice" : floatNewPrice
					}
				}
			)		
		if "UsedPrice" in latestGame:
			dbGamesHistory.update_one(
				{"_id": result.inserted_id},
				{
					"$set": {
						"UsedPrice" : floatUsedPrice
					}
				}
			)
		if "PrePrice" in latestGame:
			dbGamesHistory.update_one(
				{"_id": result.inserted_id},
				{
					"$set": {
						"PrePrice" : floatPrePrice
					}
				}
			)
	x+=1