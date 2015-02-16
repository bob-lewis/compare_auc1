__author__ = 'Bob'
import httplib2
import json
from Infograb import realmget
from Infograb import petid_get
from Infograb import write_to_master

second_round = False
r1_hi = {}
r1_lo = {}
r2_hi = {}
r2_lo = {}
PET_QUALITY = ['Trash', 'Poor', 'Common', 'Uncommon', 'Rare', 'Epic', 'Legendary']
valid_realms = ['kilrogg', 'darksorrow', 'mazrigos', 'frostwhisper']
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
				line = (' \nPossible bargain: ' + auction + ' on ' + str(cheap_server) + ' costs ' + str(buy_cost) +
				        ' and on ' + str(exp_server) + ' costs at least ' + str(sell_cost) +
				        ' \n...a potential profit of between ' + str(low_profit) + ' up to possibly ' + str(
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
	message = 'Enter ' + order + ' server name :kilrogg,darksorrow,mazrigos,frostwhisper\n>>'
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

		# print(line, '\n')
	if second_round:
		bargain_hunter(r1_hi, r1_lo, r2_lo, server_selection[1], server_selection[0])
		bargain_hunter(r2_hi, r2_lo, r1_lo, server_selection[0], server_selection[1])
		print('#' * 25)
		print('details saved to bargain_hunter.txt')

main()
