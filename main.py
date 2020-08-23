import requests
from bs4 import BeautifulSoup
import time
import os
import pandas as pd
import smtplib

url = 'https://www.ebay.com/sch/i.html?_dcat=111422&_sop=10&Release%2520Year=2020%7C2019%7C2018%7C2017%7C2016&LH_ItemCondition=1000%7C1500%7C2000%7C2500%7C3000&_fsrp=1&_sacat=0&_nkw=macbook&LH_BIN=1&_from=R40&_ipg=25&rt=nc&_udhi=700'

while True:
    results_list = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', {'class': 's-item__info clearfix'})

    for result in results:
        temp = []
        header = result.find('h3').text.replace('New Listing', '')
        mac_type = 'Pro' if 'pro' in header.lower() else 'Air' if 'air' in header.lower() else 'Reg'
        
        temp.append(result.find('span', {'class': 's-item__price'}).text)
        temp.append(header)
        temp.append(mac_type)
        
        try:
            temp.append(result.find('span', {'class': 'SECONDARY_INFO'}).text)
        except AttributeError:
            continue
        
        temp.append(result.find_all('div', {'class': 's-item__subtitle'})[-1].text)

        try:
            temp.append(result.find('span', {'class': 's-item__shipping s-item__logisticsCost'}).text)
        except AttributeError:
            temp.append('Free shipping')

        temp.append(result.find('span', {'class': 's-item__dynamic s-item__listingDate'}).text)
        results_list.append(temp)

    results_list = pd.DataFrame.from_records(results_list)

    if os.path.isfile('./curr.csv'):
        last_saved = pd.read_csv('curr.csv')
    else:
        results_list.to_csv('curr.csv', index = False)
        last_saved = pd.read_csv('curr.csv')
    try:
        similars = last_saved.iloc[:, 0] == results_list.iloc[:, 0]
    except IndexError:
        print(last_saved)
        print(results_list)
    except ValueError:
        print(last_saved)
        print(results_list)

    if any(similars):
        print(time.ctime(), 'No Updates')
        time.sleep(1)
        continue
    else:
        msg = 'Subject: {}\n\n{}'.format('New Macbook posting', 'https://www.ebay.com/sch/i.html?_dcat=111422&_sop=10&Release%2520Year=2020%7C2019%7C2018%7C2017%7C2016&LH_ItemCondition=1000%7C1500%7C2000%7C2500%7C3000&_fsrp=1&_sacat=0&_nkw=macbook&LH_BIN=1&_from=R40&_ipg=25&rt=nc&_udhi=700')
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
        results_list.to_csv('curr.csv', index = False)


    

