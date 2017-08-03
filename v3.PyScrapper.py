from pymongo import MongoClient
from lxml import html
import requests
from datetime import datetime

client = MongoClient()
db = client.test

xpath = '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/text()'
dbGames = db.games2
games = dbGames.find()
for game in games:
	gameTitle = game["GameTitle"]
	gameURL = game["EBGamesURL"]
	gamePrice = game["Price"];
	page = requests.get(gameURL)
	tree = html.fromstring(page.content)
	price = tree.xpath(xpath)	# ['$28.00', '$19.00'] OR ['$12.00']
	if price != gamePrice:		
		item = db.gamesHistory.insert(
			{
				"GameTitle": gameTitle, 
				"EBGamesURL": gameURL, 
				"Price": gamePrice,
				"Date": datetime.now().strftime(datetime.now().strftime('%Y%m%d'))
			}
		)

		#set price in db
		result = dbGames.update_one(
			{"GameTitle": gameTitle},{
				"$set": {
					"Price": price
				}
			}
		)
		
		#display game
		print('Title:\t\t',game["GameTitle"])
		print('URL:\t\t',game["EBGamesURL"])
		print('NewPrice:\t',price)
		print("")
	else:
		print('[[NotChanged]]',game["GameTitle"])

#write to file
filename = datetime.now().strftime(datetime.now().strftime('%Y%m%d.%H%M.scrap'))
gamesToFile = dbGames.find()
for game in gamesToFile:
	print('Title:\t\t',game["GameTitle"], file=open(filename, "a"))
	print('NewPrice:\t',game["Price"], file=open(filename, "a"))
	print('URL:\t\t',game["EBGamesURL"], file=open(filename, "a"))



