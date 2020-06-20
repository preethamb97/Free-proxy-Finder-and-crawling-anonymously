from userAgents import *
import requests
from cred import torKey
from bs4 import BeautifulSoup
import random
import re
import time
from stem import Signal
from stem.control import Controller

# // website all url link lists
allWebSiteUrls = []
allUrls = []
proxyList = []
fileName = 'proxy.txt'
# get new tor circuit by probability
percentageProbability = 60

def torIpCheck():
	randomNumber = random.randint(1,100)
	if (randomNumber > percentageProbability):
		renew_tor_ip()
		time.sleep(0.01)
	session = requests.session()
	proxies = {
	    'http': 'socks5h://localhost:9050',
	    'https': 'socks5h://localhost:9050'
	}
	response = session.get(r'http://www.icanhazip.com', headers = {'User-Agent': random.choice(userAgents)}, timeout=100, proxies=proxies)
	print('myTorIp :', response.text)
	time.sleep(0.00001)

def renew_tor_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password=str(torKey))
        controller.signal(Signal.NEWNYM)

def myIpRealIPCheck():
 	# response = requests.get(r'http://www.icanhazip.com', headers = {'User-Agent': random.choice(userAgents)}, timeout=100)
 	# print('myIp :', response.text)
 	# time.sleep(0.00001)
 	pass

def urlResponse(url):
	myIpRealIPCheck()
	torIpCheck()
	session = requests.session()
	proxies = {
	    'http': 'socks5h://localhost:9050',
	    'https': 'socks5h://localhost:9050'
	}
	response = session.get(url, headers = {'User-Agent': random.choice(userAgents)}, timeout=100, proxies=proxies)
	print(response)
	return response.text

def urlResponseWithTimeOut(url):
	myIpRealIPCheck()
	torIpCheck()
	session = requests.session()
	proxies = {
	    'http': 'socks5h://localhost:9050',
	    'https': 'socks5h://localhost:9050'
	}
	response = session.get(url, headers = {'User-Agent': random.choice(userAgents)}, timeout=100, proxies=proxies)
	print(response)
	return response.text

def bruteForceAllSiteUrls(url):
	response = urlResponse(url)
	soup = BeautifulSoup(response, 'html.parser')
	h3tags = soup.findAll('a')
	for a in h3tags:
		if (a.has_attr('href') and (url in str(a))):
			a=str(a)
			a=a.split('href="')[1]
			a=a.split('"')[0]
			# print(a)
			if (a not in allWebSiteUrls):
				allWebSiteUrls.append(a)

def bruteForce(url):
	counter = 0
	allWebSiteUrls.append(url)
	while  True:
		for urls in allWebSiteUrls:
			bruteForceAllSiteUrls(urls.strip())
			print('totalUrls', len(allWebSiteUrls))
			counter = counter +1 
			if counter > 1000:
				return

def getAllProxyUrls():
	for urls in allWebSiteUrls:
		response = urlResponse(urls)
		soup = BeautifulSoup(response, 'html.parser')
		h3tags = soup.findAll('a')
		for a in h3tags:
			if (a.has_attr('href') and (url in str(a)) and ("proxy-server" in str(a)) and("#" not in (str(a)))) :
				a=str(a)
				a=a.split('href="')[1]
				a=a.split('"')[0]
				# print(a)
				if (a not in allUrls):
					allUrls.append(a)

def proxyFinder(response):
	proxys = re.findall("(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3}):(?:[\d]{1,5})",str(response))
	if (proxys) and proxys is not None and proxys[0] is not None:
		return proxys

def getAllProxyLists():
	for u in allUrls:
		response = urlResponseWithTimeOut(u)
		ips = proxyFinder(response)
		for i in ips:
			appendProxyIfNotExistsInList(i)

def appendProxyIfNotExistsInList(i):
	if i not in proxyList:
		proxyList.append(i)

def dailyProxy(url):
	response = urlResponseWithTimeOut(url)
	soup = BeautifulSoup(response, 'html.parser')
	allDivs = soup.findAll('div')
	for x in allDivs:
		# print(x)
		ips = proxyFinder(x)
		if (ips):
			for y in ips:
				appendProxyIfNotExistsInList(y)

def liveSocksNet(url):
	bruteForce(url)
	# print(allWebSiteUrls)
	for val in allWebSiteUrls:
		response = urlResponse(val)
		ips = proxyFinder(response)
		if (ips):
			for i in ips:
				appendProxyIfNotExistsInList(i)

def writeToFile(proxy, fname):
	fw = open(fname, 'a')
	data = str(proxy)+'\n';
	fw.write(data)
	fw.close()

if __name__ == '__main__':
	url = "http://www.proxyserverlist24.top/".strip()
	bruteForce(url)
	getAllProxyUrls()
	print('count', len(allUrls))
	getAllProxyLists()
	#ater getting proxy empty unwanted list
	allWebSiteUrls = []
	allUrls = []
	allWebSiteUrls = []
	allUrls = []

	url = "http://proxy-daily.com/".strip()
	dailyProxy(url)

	url = "http://www.live-socks.net/".strip()
	liveSocksNet(url)
	allWebSiteUrls = []
	allUrls = []



	for i in proxyList:
		writeToFile(i, fileName)