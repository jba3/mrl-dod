####################################################################################################
# LIBRARY IMPORTING ################################################################################
####################################################################################################
# TO USE THE BEAUTIFULSOUP MODULE WITH UBUNTU:
#	sudo apt-get install python-beautifulsoup
import BeautifulSoup

# needed to use BASH curl for fetching
import subprocess

####################################################################################################
# VARIABLES ########################################################################################
####################################################################################################
filePathBase  = "/conky/python/" # base file path for storing and executing files
filePathStore = filePathBase + "results/"

mrlHomeFile = "" # read content from the file fetched externally
mrlHomeHtml = "" # content of the MRL homepage

mrlDodFile  = "" # read content from the file fetched externally
mrlDodHtml  = "" # content of the MRL Deal of the Day

urlBase  = "http://www.museumreplicas.com/" # base URL to append specific sale to
urlFetch = urlBase # full URL to fetch data from

imgCount = 0 # counter to only show the first item in images

####################################################################################################
# fetch the link for today's deal of the day #######################################################
####################################################################################################
subprocess.check_output(["bash", "-c", "curl " + urlBase + " > " + filePathStore + "mrl.html 2>&1"])

mrlHomeFile = open(filePathStore + 'mrl.html', 'r') # read content from the file fetched externally
mrlHomeHtml = BeautifulSoup.BeautifulSoup(mrlHomeFile) # content of MRL homepage

####################################################################################################
# GET THE LOCATION FOR THE DEAL OF THE DAY #########################################################
####################################################################################################
# find the div with button
for getDiv in mrlHomeHtml.findAll('div', attrs={"class": "del_cont"}):
	# first img tag is the deal of the day
	for getURL in getDiv.findAll('a'):
		# increment counter
		imgCount += 1;
		# first button
		if imgCount is 1:
			urlFetch = urlFetch + getURL['href']

####################################################################################################
# fetch the data for today's deal of the day #######################################################
####################################################################################################
subprocess.check_output(["bash", "-c", "curl " + urlFetch + " > " + filePathStore + "dod.html 2>&1"])
mrlDodFile = open(filePathStore + 'dod.html', 'r')
mrlDodHtml = BeautifulSoup.BeautifulSoup(mrlDodFile)

####################################################################################################
# now start parsing it out #########################################################################
####################################################################################################
# find the title
for getTitle in mrlDodHtml.find('h1', attrs={"itemprop": "name"}):
	print "ITEM:   " + getTitle.string
# find the retail price
for getPriceRetail in mrlDodHtml.find('span', attrs={"class": "RegularPrice"}):
	print "NORMAL: " + getPriceRetail.string.replace('Reg:&nbsp;', '')
# find the sale price
for getPriceSale in mrlDodHtml.find('span', attrs={"itemprop": "price"}):
	print "SALE:   " + getPriceSale.string
