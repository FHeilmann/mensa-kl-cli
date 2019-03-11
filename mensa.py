#!/usr/bin/env python3

import locale
import urllib.request
from bs4 import BeautifulSoup
from colorama import Style
from datetime import datetime
from contextlib import contextmanager

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

with urllib.request.urlopen("https://www.studierendenwerk-kaiserslautern.de/kaiserslautern/essen-und-trinken/tu-kaiserslautern/mensa/") as response:
    page =  response.read()
page_soup = BeautifulSoup(page, "html.parser")
daily_contents = page_soup.findAll('div', {'class' : 'dailyplan_content'})

for daily_content in daily_contents:
    date = datetime.strptime(daily_content.h5.text, '%A, %d.%m.%Y')
    if date.date() == datetime.today().date():
        print(Style.BRIGHT)
    print("=======================================")
    print(daily_content.h5.text)
    rows = daily_content.findAll('div', {'class': 'subcolumns'})
    for row in rows:
        location = row.find('div', {'class': 'subcl'})
        foods = row.find('div', {'class': 'subcr'})
        food = foods.find_all('strong')
        foodlist = []
        for fd in foods:
            try:
                if fd.text:
                    foodlist.append(fd.text)
            except AttributeError:
                pass

        print('\t'.join([location.strong.text] + ['\n\t'.join(foodlist)]))
    print("=======================================" + Style.RESET_ALL)
