#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

from db_management import DataManagement
from utils import Utils

import datetime
import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGFILE = os.path.join(BASE_DIR, 'asude.log')
logging.basicConfig(filename=LOGFILE, level=logging.INFO)

url = "https://www.msn.com/tr-tr"

response = requests.get(url)
content = response.text

now = datetime.datetime.now()
parsed_time = now.strftime("%d.%m.%Y %H:%M")

chan = BeautifulSoup(content, "lxml")
util = Utils()
data = DataManagement()

diff = {key: 0 for key, _ in data.get_statistics().items()}

isection = diff.copy()

stripes = chan.findAll('div', {'class': 'stripe'})

for stripe in stripes:
    news = stripe.findAll('li')

    for n in news:
        a_tag = n.find('a')
        href = a_tag['href']

        try:
            source = util.get_partner_url(href)
            check = data.check(href, source)
            if check:
                isection[source] = isection.get(source, 0) + 1
            else:
                diff[source] = diff.get(source, 0) + 1
                data.add_new_url(href, source)
        except:
            print(href)

print("%s tarama sonucu" % parsed_time)
logging.info("%s tarama sonucu" % parsed_time)
for source, count in data.get_statistics().items():
    print("{source} Toplam Url Sayısı: {total} - Yeni Gelen Url Sayısı: {diff} - Aynı Olan Url Sayısı: {isection}".format(
        source=source,
        total=count,
        diff=diff.get(source, 0),
        isection=isection.get(source, 0)
    ))
    logging.info("{source} Toplam Url Sayısı: {total} - Yeni Gelen Url Sayısı: {diff} - Aynı Olan Url Sayısı: {isection}".format(
        source=source,
        total=count,
        diff=diff.get(source, 0),
        isection=isection.get(source, 0)
    ))


