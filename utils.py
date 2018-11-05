#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests

import re

class Utils():
    def __init__(self):
        self.url_patt = re.compile("https?\:\/\/(www\.)?(?P<url>[\w\.\-]+)\/?")
        self.base_url = "https://www.msn.com"

        self.alt_urls = {
            'Habertürk': "https://www.haberturk.com/",
            'Goal.com': "https://www.goal.com/tr",
            'Photos': "https://www.photos.com/"
        }

    def check_img_alt(self, alt):
        for key, value in self.alt_urls.items():
            if key in alt:
                return value

        return False

    def get_partner_url(self, news_url):
        news_url = self.base_url + news_url
        response = requests.get(news_url)
        content = response.text

        news_chan = BeautifulSoup(content, "lxml")
        partner = news_chan.find('span', {'class': 'partner'})
        if not partner:
            partner = news_chan.find('div', {'class': 'content'})

        partner_url = partner.find('a')
        if partner_url:
            partner_url = partner_url['href']
        else:
            img_alt = partner.find('img')['alt']
            partner_url = self.check_img_alt(img_alt)
            if not partner_url:
                print("Not parsed source url: %s" % news_url)

        clean_url = self.url_patt.search(partner_url)
        if clean_url:
            clean_url = clean_url.group('url')
            return clean_url
        else:
            img_alt = partner.find('img')['alt']
            partner_url = self.check_img_alt(img_alt)
            if not partner_url:
                print("Regex crashed: %s" % news_url)
                return False
            else:
                clean_url = self.url_patt.search(partner_url)
                clean_url = clean_url.group('url')
                return clean_url
