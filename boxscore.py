import requests
from bs4 import BeautifulSoup

def getBoxScoreData(game_id):
	url = 'http://www.nhl.com/gamecenter/en/boxscore?id='+str(game_id)
	soup = BeautifulSoup(requests.get(url).text, 'html.parser')
	
	#Retrieve the data table HTML area from boxscore, must include stats table
	tableAreaHTML = [area for area in soup.find_all('div', class_='contentPad') if len(area.find_all('table', class_='stats')) > 0]

	#Remove the list property
	if len(tableAreaHTML) == 1:
		tableAreaHTML = tableAreaHTML[0]
	else:
		raise ValueError('Did not find data tables in HTML')

	#Find the headers for the table and initialize variables
	tableHeaders = tableAreaHTML.find_all('div', class_='primary tableHeader')
	rwPlayerTable = 0
	rwGoalieTable = 0
	firstTable = True

	#Find the tables for the red wings
	for i, header in enumerate(tableHeaders):
		if(header.find('a').string[0:7] == 'Detroit'):
			if firstTable:
				rwPlayerTable = i
				firstTable = False
			else:
				rwGoalieTable = i

	#Tables follow the headers
	playerTable = tableHeaders[rwPlayerTable].nextSibling
	goalieTable = tableHeaders[rwGoalieTable].nextSibling
	
	playerData = []
	goalieData = []

	#Iterate through row HTML and extract the data
	playerRows = playerTable.find_all('tr')
	for row in playerRows:
		data = [ stat.string for stat in row.children]
		if data[0] != 'No.': #Identifier for header
			playerData.append(data)

	goalieRows = goalieTable.find_all('tr')
	for row in goalieRows:
		data = [ stat.string for stat in row.children]

		#Fix for NHL handeling goalie wins
		if data[1] == None:
			data[1] = row.find('a').string

		if data[0] != 'No.':
			goalieData.append(data)

	return (playerData, goalieData)
	
	

def main():
	a = getBoxScoreData(2015020014)
	print(a)


if __name__ == '__main__':
	main()