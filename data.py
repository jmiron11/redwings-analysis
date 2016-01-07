import shelve
import boxscore


# Data layout in rawData:
#
#	{ game_id: game_data }
# game_data = (player_data, goalie_data)
# player_data = [#, name, pos, G, A, P, +-, PIM, S, Hits, BKS, GVA, TKA, FO%, PPTOI, SHTOI, TOI]
#

shelf_name = 'raw-redwings-data'


#Adds the data to the dictionary stored in shelved-stats
def updateShelf(game_id, newData):
	d = shelve.open(shelf_name)

	data = d['raw']

	#Add the new data to the dictionary and store it
	data[game_id] = newData
	d['raw'] = data

	d.close()


def initData():
	ids = boxscore.getAllBoxScoreIds()

	rawData = {}

	for game_id in ids:
		rawData[int(game_id)] = boxscore.getBoxScoreData(game_id)

	# store the data
	d = shelve.open(shelf_name)
	d['raw'] = rawData
	d.close()

def getRawData():
	d = shelve.open(shelf_name)

	rawData = d['raw']

	d.close()
	return rawData


def main():
	rawData = getRawData()
	print(rawData['2015020014'])
	# initData()




if __name__ == '__main__':
	main()