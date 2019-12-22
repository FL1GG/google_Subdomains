import requests
import re
from time import sleep

#sysarg1
sitesearch = "site.com"
waittime = 10


#init
f = open(sitesearch + ".txt", "w")

sitetop = sitesearch.split(".")[-1]
sitemid = sitesearch.split(".")[-2]
r = requests.session()
suddomains = set([])
newsubs = set([])
rounds = 0

"""
========================
Google Search
========================
"""

regurlmatch = r"https?://(.*?)\." + re.escape(sitetop)
baseurl = "https://google.com/search?q="
urlupdate = baseurl+"site:" + sitesearch


while True:

    result = r.get(urlupdate)

    if("- did not match any documents." in result.text):
        break
    if(result.status_code == 429):
        print("Google search failed, too many requests at once. {0} Subdomains Salvaged.".format(len(suddomains)))
        break
    links = re.findall(regurlmatch, result.text)

    for link in links:
        if(sitemid in link):
            suddomains.add(link + "." + sitetop)
            newsubs.add(link.replace("." + sitemid, ""))

    for i in newsubs:
        urlupdate = urlupdate + "+-inurl:" + i

    newsubs = set([])
    sleep(waittime)

    rounds += 1
    if(rounds % 10 == 0):
        print("Round {0}: {1} Subdomains found from Google".format(rounds, len(suddomains)))

print("Google Search Completed")

"""
==============
Finish
==============
"""
for i in suddomains:
    f.write(i + "\n")
