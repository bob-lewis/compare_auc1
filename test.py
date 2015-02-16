__author__ = 'Bob'
import json
import os

import httplib2

from Infograb import realmget
from Infograb import petid_get
from Infograb import write_to_master


second_round = False
r1_hi = {}
r1_lo = {}
r2_hi = {}
r2_lo = {}
PET_QUALITY = ['Trash', 'Poor', 'Common', 'Uncommon', 'Rare', 'Epic', 'Legendary']
valid_realms = valid_realms = ['aegwynn', 'aerie-peak', 'agamaggan', 'aggra-portugues', 'aggramar', 'ahnqiraj',
                               'alakir', 'alexstrasza', 'alleria', 'alonsus', 'amanthul', 'ambossar', 'anachronos',
                               'anetheron', 'antonidas', 'anubarak', 'arakarahm', 'arathi', 'arathor', 'archimonde',
                               'area-52', 'argent-dawn', 'arthas', 'arygos', 'ashenvale', 'aszune', 'auchindoun',
                               'azjolnerub', 'azshara', 'azuregos', 'azuremyst', 'baelgun', 'balnazzar', 'blackhand',
                               'blackmoore', 'blackrock', 'blackscar', 'blades-edge', 'bladefist', 'bloodfeather',
                               'bloodhoof', 'bloodscalp', 'blutkessel', 'booty-bay', 'borean-tundra', 'boulderfist',
                               'bronze-dragonflight', 'bronzebeard', 'burning-blade', 'burning-steppes', 'cthun',
                               'chamber-of-aspects', 'chants-eternels', 'chogall', 'chromaggus', 'colinas-pardas',
                               'confrerie-du-thorium', 'conseil-des-ombres', 'crushridge', 'culte-de-la-rive-noire',
                               'daggerspine', 'dalaran', 'dalvengyr', 'darkmoon-faire', 'darksorrow', 'darkspear',
                               'das-konsortium', 'das-syndikat', 'deathguard', 'deathweaver', 'deathwing', 'deepholm',
                               'defias-brotherhood', 'dentarg', 'der-mithrilorden', 'der-rat-von-dalaran',
                               'der-abyssische-rat', 'destromath', 'dethecus', 'die-aldor', 'die-arguswacht',
                               'die-nachtwache', 'die-silberne-hand', 'die-todeskrallen', 'die-ewige-wacht',
                               'doomhammer', 'draenor', 'dragonblight', 'dragonmaw', 'drakthul', 'drekthar', 'dun-modr',
                               'dun-morogh', 'dunemaul', 'durotan', 'earthen-ring', 'echsenkessel', 'eitrigg',
                               'eldrethalas', 'elune', 'emerald-dream', 'emeriss', 'eonar', 'eredar', 'eversong',
                               'executus', 'exodar', 'festung-der-sturme', 'fordragon', 'forscherliga', 'frostmane',
                               'frostmourne', 'frostwhisper', 'frostwolf', 'galakrond', 'garona', 'garrosh', 'genjuros',
                               'ghostlands', 'gilneas', 'goldrinn', 'gordunni', 'gorgonnash', 'greymane', 'grim-batol',
                               'grom', 'guldan', 'hakkar', 'haomarush', 'hellfire', 'hellscream', 'howling-fjord',
                               'hyjal', 'illidan', 'jaedenar', 'kaelthas', 'karazhan', 'kargath', 'kazzak', 'kelthuzad',
                               'khadgar', 'khaz-modan', 'khazgoroth', 'kiljaeden', 'kilrogg', 'kirin-tor', 'korgall',
                               'kragjin', 'krasus', 'kul-tiras', 'kult-der-verdammten', 'la-croisade-ecarlate',
                               'laughing-skull', 'les-clairvoyants', 'les-sentinelles', 'lich-king', 'lightbringer',
                               'lightnings-blade', 'lordaeron', 'los-errantes', 'lothar', 'madmortem', 'magtheridon',
                               'malganis', 'malfurion', 'malorne', 'malygos', 'mannoroth', 'marecage-de-zangar',
                               'mazrigos', 'medivh', 'minahonda', 'moonglade', 'mugthol', 'nagrand', 'nathrezim',
                               'naxxramas', 'nazjatar', 'nefarian', 'nemesis', 'neptulon', 'nerzhul', 'nerathor',
                               'nethersturm', 'nordrassil', 'norgannon', 'nozdormu', 'onyxia', 'outland', 'perenolde',
                               'pozzo-delleternita', 'proudmoore', 'quelthalas', 'ragnaros', 'rajaxx', 'rashgarroth',
                               'ravencrest', 'ravenholdt', 'razuvious', 'rexxar', 'runetotem', 'sanguino', 'sargeras',
                               'saurfang', 'scarshield-legion', 'senjin', 'shadowsong', 'shattered-halls',
                               'shattered-hand', 'shattrath', 'shendralar', 'silvermoon', 'sinstralis', 'skullcrusher',
                               'soulflayer', 'spinebreaker', 'sporeggar', 'steamwheedle-cartel', 'stormrage',
                               'stormreaver', 'stormscale', 'sunstrider', 'sylvanas', 'taerar', 'talnivarr',
                               'tarren-mill', 'teldrassil', 'temple-noir', 'terenas', 'terokkar', 'terrordar',
                               'the-maelstrom', 'the-shatar', 'the-venture-co', 'theradras', 'thermaplugg', 'thrall',
                               'throkferoth', 'thunderhorn', 'tichondrius', 'tirion', 'todeswache', 'trollbane',
                               'turalyon', 'twilights-hammer', 'twisting-nether', 'tyrande', 'uldaman', 'ulduar',
                               'uldum', 'ungoro', 'varimathras', 'vashj', 'veklor', 'veknilash', 'voljin', 'wildhammer',
                               'wrathbringer', 'xavius', 'ysera', 'ysondre', 'zenedar', 'zirkel-des-cenarius', 'zuljin',
                               'zuluhed']

spinner = '||//--\\\\'
server_selection = []


def bargain_hunter(sell_server_hi, sell_server_lo, buy_server, cheap_server, exp_server):
	bargains = []
	for auction in sell_server_lo:
		if auction in buy_server:
			if buy_server[auction] < sell_server_lo[auction]:
				sell_cost = sell_server_lo[auction]
				buy_cost = buy_server[auction]
				low_profit = (sell_server_lo[auction] - buy_server[auction])
				high_profit = (sell_server_hi[auction] - buy_server[auction])
				line = (' \nPossible bargain: ' + auction + ' on ' + str(cheap_server) + ' costs ' + str(
					buy_cost) + ' and on ' + str(exp_server) + ' costs at least ' + str(
					sell_cost) + ' \n...a potential profit of between ' + str(low_profit) + ' up to possibly ' + str(
					high_profit) + ' \n' + '*' * 20)
				bargains.append(line)
	write_to_master(bargains)


def page_get(server):
	print(str('http://eu.battle.net/api/wow/auction/data/' + server))
	request = str('http://eu.battle.net/api/wow/auction/data/' + server)
	h = httplib2.Http(".cache")
	content_headers, content = h.request(request)
	content = content.decode()
	obj = json.loads(content)
	for key, value in obj.items():
		x = (value[0])
		return (x['url'])


def quickspinner(n):
	print(spinner[n - 1], end='\r')


def get_server():
	if second_round == True:
		order = 'second'
	else:
		order = 'first'
	print('We need two server names, enter them when asked ,they are case sensitive')
	message = 'Enter ' + order + ' server name eg :kilrogg,darksorrow,mazrigos,frostwhisper,alakir,aerie-peak etc \n>>'
	server = str(input(str(message)))
	server_selection.append(server)
	if server in valid_realms:
		return (page_get(server))
	else:
		server = 'kilrogg'
		print('Not a valid server, using default, kilrogg..\n.....\n..........')
		return (page_get(server))


def main():
	global second_round, server1

	server1 = get_server()
	print('Accessing\n', server1)
	create_pet_auction_lists(realmget(server1))
	second_round = True
	server2 = get_server()
	print('Accessing\n', server2)
	create_pet_auction_lists(realmget(server2))


def create_pet_auction_lists(realm):
	if second_round == False:
		hi = r1_hi
		lo = r1_lo
	else:
		hi = r2_hi
		lo = r2_lo

	working_list = []
	count = 0
	for line in realm:
		working_list_temp_line = []
		if line[1] == 'item:82800':
			working_list_temp_line.append(line[2])
			working_list_temp_line.append(line[3])
			cost_adjust = str(line[5]).partition(':')[2]
			cost = (int(cost_adjust) / 10000)
			cost = float("{0:.2f}".format(cost))
			working_list_temp_line.append(cost)
			check = str(line[17])
			check = check.partition(':')[2]
			id = petid_get(check)
			quality = str(line[20])
			quality = quality.partition(':')[2]
			qualnumber = (int(quality))
			quality = PET_QUALITY[qualnumber]
			petname = str(id + ' of ' + quality + ' quality.')
			working_list_temp_line.append(petname)
			working_list_temp_line.append(line[18])
			working_list.append(working_list_temp_line)
			quickspinner(count)
			if count > (len(spinner) - 1):
				count = 0
			else:
				count += 1

	for line in working_list:
		name = str(line[3])
		price = int(line[2])
		if name in hi:
			if price > hi[name]:
				hi[name] = price
			else:
				pass
		else:
			hi[name] = price
		if name in lo:
			if price < lo[name]:
				lo[name] = price
			else:
				pass
		else:
			lo[name] = price

	if second_round:
		bargain_hunter(r1_hi, r1_lo, r2_lo, server_selection[1], server_selection[0])
		bargain_hunter(r2_hi, r2_lo, r1_lo, server_selection[0], server_selection[1])
		print('#' * 25)
		print('details saved to bargain_hunter.txt')


main()

try:
	os.remove("bargains.txt")
except:
	os.rename("temp.txt", "bargains.txt ")
os.rename("temp.txt", "bargains.txt ")