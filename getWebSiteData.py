from userAgents import *
import requests
from cred import torKey
from bs4 import BeautifulSoup
import random
import re
import time
from stem import Signal
from stem.control import Controller
import ssl

percentageProbability = 60
websiteUrl = ""
websiteAllUrls = []
checkedUrls = []
def torRequest(url):
	randomNumber = random.randint(1,100)
	# if (randomNumber > percentageProbability):
	getNewTorIdentity()
	session = requests.session()
	proxies = {
	    'http': 'socks5h://localhost:9050',
	    'https': 'socks5h://localhost:9050'
	}
	response = session.get(url, headers = {'User-Agent': random.choice(userAgents)}, timeout=100, proxies=proxies)
	print(response)
	return response.text

def getNewTorIdentity():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password=str(torKey))
        controller.signal(Signal.NEWNYM)

def soupRequests(response):
	soup = BeautifulSoup(response,"html.parser")
	for a in soup.find_all('a'):
		if a.has_attr('href'):
			try:
				a = str(a)
				a = a.split('href="')[1].split('"')[0]
				a = a.split('"')[0].split('"')[0]
				if "://" not in a:
					if a[0] != "/":
						a = "/" + a
					a = websiteUrl + a
				if (a not in websiteAllUrls) and (websiteUrl in a):
					if (a!=websiteUrl + "/") and (a != websiteUrl):
						websiteAllUrls.append(a)
			except Exception as e:
				print(e)

def getWebsiteLinks(url):
	response = torRequest(url)
	soupRequests(response)

def writeToFile(link, fname):
	fw = open(fname, 'a')
	data = str(link)+'\n';
	fw.write(data)
	fw.close()

if __name__ == '__main__':
	websiteUrl = (input("Enter the website url : ")).strip()
	getWebsiteLinks(websiteUrl)
	if websiteUrl[len(websiteUrl) - 1] == '/':
		websiteUrl = websiteUrl[0:len(websiteUrl) - 1]
	while True:
		counter = 0
		for i in websiteAllUrls:
			if i not in checkedUrls:
				getWebsiteLinks(i)
				checkedUrls.append(i)
				counter = counter + 1
		if counter = 0:
			break
	filename = str(websiteUrl) + '.txt'
	for i in websiteAllUrls:
		writeToFile(i, filename)

