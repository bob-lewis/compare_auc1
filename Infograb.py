__author__ = 'Bob'
# comparethemurloc module to grab data from api address
import httplib2, string, json


def petid_get(id):
	newid = id.replace(":", "")
	request = str('http://eu.battle.net/api/wow/battlePet/species/' + newid)
	# print(request)
	h = httplib2.Http(".cache")
	content_headers, content = h.request(request)
	content = content.decode()
	obj = json.loads(content)
	#for key,value in obj.items():
	#   x = (key)
	#print (obj)
	if 'creatureId' in obj:
		#print (obj['name'])
		return (obj['name'])
	else:

		return 'unknown pet'


def realmget(auc_api):
	auc_list = []
	print('Calculating ,please wait')
	h = httplib2.Http(".cache")
	content_headers, content = h.request(auc_api)
	content = content.decode().split('\n')
	auc_list = []  # below is there pretty much to get around not being able to convert directly from json>list , will fix
	for line in content:
		line = line.replace("'", '').replace('{', '').replace('}', '').replace('"', '')
		detail = line.strip().split(",")
		auc_list.append(detail)
	auc_list = list(auc_list[3:-1])
	# write_to_master(auc_list)
	return (auc_list)


def main():
	auc_api = 'None'

	realmget(auc_api)


def write_to_master(auc_list):
	with open('temp.txt', 'a') as master:
		for line in auc_list:
			master.write(str(line))

	print('details written to bargains.txt')


if __name__ == '__main__':
	main()