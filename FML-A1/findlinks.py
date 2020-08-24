import re
from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing import Pool, Manager

# store all the hotel links for more detail about the individualt hotels in a set.
base = []
f = open("countries.txt", "r")
for x in f:
	base.append(x[:-1])
f.close()

urls = []
urls.extend(base)

for i in base:
	c = 1
	while(c < 5):
		temp = i + '&rows=25&offset=' + str(25*c)
		urls.append(temp)
		c += 1

manager = Manager()
hrefs = manager.list()


def add(url):
	browser = webdriver.Chrome()
	print("exploring " + url + "...")
	browser.get(url)
	response = browser.page_source
	browser.close()
	soup = BeautifulSoup(response, 'lxml')

	ROI = soup.findAll(href=re.compile('/hotel/(.)*.html'))

	for i in ROI:
		if i.get("href")[0] == '/':
			hrefs.append(re.findall(r'\/hotel\/.*\.html', i.get("href"))[0])


p = Pool(8)
p.map(add, urls)
p.terminate()
p.join()

unique_hrefs = set(hrefs)
size = len(unique_hrefs)
print("found "+ str(size) + " unique hotel links")
print("Adding all the links into \"urls.txt\" file ... ")
f = open("urls.txt",'w')
for x in unique_hrefs:
	f.write(str(x) + "\n")
f.close()
print("links added to \"urls.txt\" file")