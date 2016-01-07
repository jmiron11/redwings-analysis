import requests
from bs4 import BeautifulSoup


def getAllBoxScoreIds():
	#URL of detroit schedule page with links to boxscores
	url = 'http://www.nhl.com/ice/schedulebyseason.htm?team=DET'

	#Parse for the id within the links
	soup = BeautifulSoup(requests.get(url).text, 'html.parser')

	# print(a)
	boxscoreLinks = [a['href'] for a in soup.find_all('a') if a.span != None and 'RECAP' in a.span.string]

	ids = []
	for link in boxscoreLinks:
		ids.append(link[len(link)-10:])

	return ids


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

	convertToBuiltin(playerData,'player')
	convertToBuiltin(goalieData,'goalie')

	return (playerData, goalieData)
	
def convertToBuiltin(data, pos):
	if pos == 'player':
		# Turn the data into native python elements
		for row in data:
			row[0] = int(row[0]) #no.
			row[1] = str(row[1]) #name
			row[2] = str(row[2]) #pos

			#int stats
			for i in range(3, 13):
				row[i] = int(row[i])
			
			#FO%
			if row[13] == '-':
				row[13] = None
			else:
				row[13] = int(str(row[13]).replace('%', ''))

			row[14] = str(row[14])
			row[15] = str(row[15])
			row[16] = str(row[16])

	elif pos == 'goalie':
		for row in data:
			row[0] = int(row[0]) #no.
			row[1] = str(row[1]) #name
			row[2] = str(row[2]) #ev
			row[3] = str(row[3]) #pp
			row[4] = str(row[4]) #sh
			row[5] = str(row[5]) #saves-shots
			row[6] = float(row[6])
			row[7] = int(row[7])
			row[8] = str(row[8])




def main():
	data = getBoxScoreData(2015020014)
	for i in range(0, 9):
		print(type(data[1][0][i]))

if __name__ == '__main__':
	main()