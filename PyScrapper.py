#add support for pre-release games
##record only single price, the lower price (regardless new or preowned)
##test adding a new item to db with 0 price works without flushing all data

from pymongo import MongoClient
from lxml import html
import requests
from datetime import datetime

client = MongoClient()
db = client.test

xpath = '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/text()'
xpathPreRelease = '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[2]/text()'

dbGames = db.games4
dbGamesHistory = db.gamesHistory4

games = dbGames.find()
for game in games:
	gameTitle = game["GameTitle"]
	gameURL = game["EBGamesURL"]
	gamePrice = game["Price"];
	page = requests.get(gameURL)
	tree = html.fromstring(page.content)
	price = tree.xpath(xpath)	# ['$28.00', '$19.00'] OR ['$12.00'] OR [] (in case of PreRelease checked by xpath not xpathPreRelease

	if price == []:
		#price was empty, use PreRelease xpath
		price = tree.xpath(xpathPreRelease)
	
	if len(price) > 1:
		lowest_price = price[0] if price[0] < price[1] else price[1]
	else:
		lowest_price = price[0]	
	
	if lowest_price != gamePrice:
		item = dbGamesHistory.insert(
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
					"Price": lowest_price
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
filename = datetime.now().strftime(datetime.now().strftime('v4%Y%m%d.%H%M.scrap'))
gamesToFile = dbGames.find()
for game in gamesToFile:
	print(game["Price"],'\t',game["GameTitle"], file=open(filename, "a"))