import requests
from bs4 import BeautifulSoup
import time
import os
import pandas as pd
import smtplib

url = 'https://www.ebay.com/sch/i.html?_dcat=111422&_sop=10&Release%2520Year=2020%7C2019%7C2018%7C2017%7C2016&LH_ItemCondition=1000%7C1500%7C2000%7C2500%7C3000&_fsrp=1&_sacat=0&_nkw=macbook&LH_BIN=1&_from=R40&_ipg=25&rt=nc&_udhi=700'
last_saved = None
while True:
    results_list = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    headers = [header.text.replace('New Listing', '') for header in soup.find_all('h3', {'class': 's-item__title'})]
    
    if last_saved is None:
        last_saved = headers
        continue

    # print(last_saved)
    # print(headers)

    if last_saved == headers:
        print(time.ctime(), 'No Updates')
        # time.sleep(1)
        continue
    else:
        msg = 'Subject: {}\n\n{}'.format('New eBay posting', 'https://www.ebay.com/sch/i.html?_dcat=111422&_sop=10&Release%2520Year=2020%7C2019%7C2018%7C2017%7C2016&LH_ItemCondition=1000%7C1500%7C2000%7C2500%7C3000&_fsrp=1&_sacat=0&_nkw=macbook&LH_BIN=1&_from=R40&_ipg=25&rt=nc&_udhi=700')
        fromaddr = 'YOUR_EMAIL_ADDRESS'
        toaddrs  = ['RECIPIENT_EMAIL_ADDRESS']

        print(time.ctime(), 'Please check email')

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("YOUR_EMAIL_ADDRESS", "YOUR_EMAIL_PASSWORD")
        server.sendmail(fromaddr, toaddrs, msg)
        # disconnect from the server
        server.quit()

        print('Email Sent')
        print(headers)
        last_saved = headers
    

