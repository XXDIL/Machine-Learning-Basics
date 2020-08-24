import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
from multiprocessing import Pool, Manager

# URL's we will scrape
base_url = "https://www.booking.com"

# data we will be collection
manager = Manager()
names = manager.list()
stars = manager.list()
city = manager.list()
state = manager.list()
country = manager.list()
# price = manager.list()
amenities = manager.list()
description = manager.list()
review1 = manager.list()
review2 = manager.list()

def scrape(href):

	# traverse the set and now DFS all the way to the hotels.
	url = base_url + href
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'lxml')

	print(url)

	n = soup.find("div", {"class": "hp__hotel-title"}).getText().strip().split('\n')[1]
	s = soup.find("span", {"class": "invisible_spoken"}).getText()[0]
	if(s > '5'):
		s = 'NaN'
	loc = soup.findAll("div", {"class": "bui-breadcrumb__text"})
	desc = soup.find("div", {"id" : "property_description_content"}).getText().strip()
	review = soup.findAll("span", {"class":"c-review__body"})												
	ammens = soup.find("div", {"class":"facilitiesChecklist"}).getText().strip('\n').split('\n')

	if review == []:
		review.append(BeautifulSoup('NaN', 'lxml'))
		review.append(BeautifulSoup('NaN', 'lxml'))

	if (loc[4].getText().split('\n')[2] == ""):
		city.append('NaN')
	else:
		city.append(loc[4].getText().split('\n')[2])			# city

	if (loc[3].getText().split('\n')[2] == ""):
		state.append('NaN')
	else:
		state.append(loc[3].getText().split('\n')[2])			# state

	if (loc[2].getText().split('\n')[2] == ""):
		country.append('NaN')
	else:
		country.append(loc[2].getText().split('\n')[2])			# country

	names.append(n) 											# name
	stars.append(s)												# stars
	description.append(desc)									# description
	review1.append(review[0].getText())							# review 1
	review2.append(review[1].getText())							# review 2
	amenities.append(list(filter(('').__ne__, ammens)))			# amenities

	percent = (len(names)/size) * 100
	if(percent >= 25 and int(percent) % 25 == 0):
		print(str(percent) + '%')


hrefs = []
f = open("urls.txt", "r")
for i in f:
	hrefs.append(i[:-1])
f.close()

size = len(hrefs)

print("Database Contains : "+ str(size) +" Hotels....\n")
print("Starting data collection from " + str(size) + " hotels.... \n")

p = Pool(10)
p.map(scrape, hrefs)
p.terminate()
p.join()

# insert into the dataframe
df_names = list(names)
df_stars = list(stars)
df_city = list(city)
df_state = list(state)
df_country = list(country)
# df_price = list(price)
df_amenities = list(amenities)
df_description = list(description)
df_review1 = list(review1)
df_review2 = list(review2)

hotel_details = pd.DataFrame({"Name":df_names, "City":df_city, "State":df_state, "Country":df_country, "Description":df_description, "Stars":df_stars, "Amenities":df_amenities, "Review1":df_review1, "Review2":df_review2})
hotel_details.to_csv("DATA.csv")