import data

# Data layout in rawData:
#
#	{ game_id: game_data }
# game_data = (player_data, goalie_data)
# player_data = [#, name, pos, G, A, P, +-, PIM, S, Hits, BKS, GVA, TKA, FO%, PPTOI, SHTOI, TOI]
#


def idx(stat):
	mapping = {'#':0,
						 'name': 1,
						 'pos': 2,
						 'G': 3,
						 'A': 4,
						 'P': 5,
						 '+-': 6,
						 'PIM': 7,
						 'S': 8,
						 'Hits': 9,
						 'BKS': 10,
						 'GVA': 11,
						 'TKA': 12,
						 'FO%': 13,
						 'PPTOI': 14,
						 'SHTOI': 15,
						 'TOI': 16}
	
	if stat not in mapping:
		print(stat + 'Is not a valid statistic')
		return -1
	else:
		return mapping[stat]


#playerName: Format - D. Larkin (FirstInitial. LastName)
#stat:  must be a valid stat as indexed by the idx() function
def getValues(playerName, stat):
	rawData = data.getRawData()

	values = []
	for i, game_id in enumerate(rawData):
		playedInGame = False
		for player in rawData[game_id][0]:
			if player[idx('name')] == playerName:
				values.append((player[idx(stat)], i+1))
				playedInGame = True
		if playedInGame == False:
			values.append((None, i+1))

	return values


def main():
	values = getValues('D. Larkin', 'TOI')
	print(values)



if __name__ == '__main__':
	main()