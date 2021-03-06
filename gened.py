import pickle
import requests
from bs4 import BeautifulSoup


def get_new_list():	# function return new list updated from UMass website
	URL = 'https://www.umass.edu/registrar/students/general-educationacademic-requirements/gen-ed-list'
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')
	result = soup.find('table', style='width:594px') # find the target table (gen-ed courses)
	rows = result.find_all('tr') # get all the rows from the table
	list = {} # create a list of gen-ed classes (nested dictionary) each class number corresponds to one class
	for row in rows:
		entry = row.find_all('td')
		category = entry[0].text.strip()
		number = entry[1].text.strip()
		name = entry[2].text.strip()					#list {
		if number not in list:							#	"AFROAM 118"{ # start of an entry (I call it number for course number)
			list[number] = {}							#		"name" : "Survey of Afro-American Lit II",
			list[number]["name"] = name					#		"category" : "ALDU"
			list[number]["category"] = category			#	} # end of an entry
		else:											#	...
			list[number]["category"] += category		#} # end of list
	return list


def read(): # read the dict from .dat file, if not found create one
	try:
		file = open('gened.dat', 'rb')
		list = pickle.load(file)
		file.close()
		return list
	except FileNotFoundError:
		print("File \"gened.dat\" is not found and will be created.")
		list = get_new_list()
		write(list)
		return list


def write(list): # write the dictionary to a .dat file
    file = open("gened.dat", "wb")
    pickle.dump(list, file)
    file.close()


def write_to_file(list): # write the dictionary to a text file
	f = open("gened.txt", "w")
	for number, info in list.items():
		f.write("\nnumber: %s" %number)
		for key in info:
			f.write("\n%s: %s" %(key, info[key]))
		f.write("\n")
	f.close() 


def get_by_category(list, category):
	category = category.upper()
	newlist = {}
	for number, info in list.items():
		if category in info["category"]:
			newlist[number] = {}
			newlist[number]["name"] = info["name"]
			newlist[number]["category"] = info["category"]
	return newlist


def get_double_category(list, category):
	category = category.upper()
	newlist = {}
	for number, info in list.items():
		if category in info["category"] and len(info["category"]) == 4:
			newlist[number] = {}
			newlist[number]["name"] = info["name"]
			newlist[number]["category"] = info["category"]
	return newlist


# -------------------------- testing area -------------------------------

# read from database (pre-scraped)
list = read()

# update database from website (new scrape)
# write(get_new_list())

# print entire gen-ed list to terminal
# for name, info in list.items():
#     print("\nname:", name)
#     for key in info:
#         print(key + ':', info[key])

# write the entire gen-ed list into text file
# write_to_file(list)

# get a list of gen-ed that satisfies AL
# get_by_category(list, "AL")

# write search result to text file
write_to_file(get_double_category(list, "DU"))