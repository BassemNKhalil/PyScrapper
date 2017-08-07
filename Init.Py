from pymongo import MongoClient
from lxml import html
import requests
from datetime import datetime

client = MongoClient()
db = client.test

xpathTitle			= '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/h1/text()'

dbGames = db.games
dbURLs = db.URLs

URLs = dbURLs.find()
for URL in URLs:
	page 		= requests.get(URL["EBGamesURL"])
	tree 		= html.fromstring(page.content)
	title		= tree.xpath(xpathTitle)[0].replace('(preowned)', '').strip()

	gameCount = dbGames.find({"GameTitle":title}).count()
	if gameCount == 0:
		print("Found")
		result = dbGames.insert_one(
			{
				"GameTitle": title,
				"EBGamesURL": URL["EBGamesURL"],
			}
		)