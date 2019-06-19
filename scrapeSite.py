# Parameters
rootPage = "https://docs.microsoft.com/en-us/azure/#pivot=products&panel=all"
chromeDriver = "C:\Program Files (x86)\python2\Lib\site-packages\chromedriver\chromedriver.exe"
downloadsDirSubDir = 'docs'

# Import Libraries
import re
import wget
import urllib2
import os
import os.path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Build Arrays, Variables, and Lists
childPages = []
downloadList = []
downloadDir = os.environ['userprofile'] + "\\Downloads\\" + downloadsDirSubDir

# Define Web Driver
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chromeDriver,chrome_options=options)

# Get Root List of Products
#   Get Page and Pull only Product Listings Tiles

driver.get(rootPage)
soupRoot = BeautifulSoup(driver.page_source,"html.parser")

#   Filter and Cleanup Links for Each Tile
for aL in soupRoot.find_all('a', href=True):
    if "/en-us/azure" in aL['href']:
        if "https" not in aL['href']:
            temp = "https://docs.microsoft.com" + aL['href']
            print temp
            childPages.append(temp)
        else:
            print aL['href']
            childPages.append(aL['href'])
    elif "https://docs.microsoft.com/azure" in aL['href']:
        childPages.append(aL['href'])
    else:
        continue

# Get Download Links from Child Pages
for bL in childPages:
    x = 0
    while (x < 10):
        try:
            driver.get(bL)
        except:
            print "Retrying " + bL
            x = x + 1 
            continue
        break
    childPageCont = driver.page_source
    bSoup = BeautifulSoup(childPageCont)
    bLinkList = bSoup.find_all('a', href=True)
    #print bLinkList
    #bLinkList
    for bL2 in bLinkList:
        if "opbuildpdf" in bL2['href']:
            if bL2['href'] not in downloadList:
                downloadList.append(bL2['href'])
                print bL2['href']

# Choose Target File Name and Download Files
for dl in downloadList:
    name = re.sub(r"\?.*$","",dl)
    name = name[38:-8]
    name = name.lstrip("-stack")
    name = name.replace("/opbuildpdf","")
    name = name.lstrip("/")
    name = name.replace("/","_")
    name = downloadDir + "\\" + name + ".pdf"
    print name
    if os.path.isfile((name)):
        print name + " already downloaded"
    else:
        wget.download(dl,name)

