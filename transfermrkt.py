import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
import re
import json

k = 1

dict_data = {}

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = "https://www.transfermarkt.com/lionel-messi/leistungsdatendetails/spieler/28003/saison//verein/0/liga/1/wettbewerb//pos/0/trainer_id/0/plus/1"
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

tbody = pageSoup.find_all('tbody')
rows = tbody[2].find_all('tr')

for r in rows:

	if r.has_attr('class'):
		match_data = []
		match = r.find_all('td')
		for i in match:
			match_data.append(i.text)
		match_data = match_data[1:]

		dict_data[k] = { # ADDING MATCH META DATA
				'date': match_data[0],
				'hometeam': re.sub('\\.+','', match_data[2]),
				'awayteam': re.sub('\\.+','', match_data[4]),
				'result': match_data[5]}

		if len(r['class']) == 0: # PLAYED IN THE MATCH
			
			dict_data[k]['position'] = re.sub('\\.+','', match_data[6])
			dict_data[k]['goals'] = match_data[7]
			dict_data[k]['assists'] = match_data[8]
			dict_data[k]['owngoals'] = match_data[9]
			dict_data[k]['yellowcards'] = match_data[10]
			dict_data[k]['secondyelcard'] = match_data[11]
			dict_data[k]['redcard'] = match_data[12]
			dict_data[k]['sub_on'] = match_data[13]
			dict_data[k]['sub_off'] = match_data[14]
			dict_data[k]['minsplayed'] = match_data[15]
			

		elif r['class'][0] == 'bg_rot_20': # NOT IN SQUAD / INJURED

			dict_data[k]['position'] = 'PLAYER NOT IN SQUAD'

		elif r['class'][0] == 'bg_gelb_20': # ON THE BENCH

			dict_data[k]['position'] = 'Player on the bench'
			

	k += 1


with open('results.json', 'w') as f:
	json.dump(dict_data, f, indent = 4)

