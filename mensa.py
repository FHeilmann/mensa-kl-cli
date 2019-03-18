#!/usr/bin/env python3
"""Terminal application to grab and display the food plan of
   the TU KL mensa
"""
import os
import re
import glob
import urllib.request
from datetime import datetime
from contextlib import contextmanager

import click
from halo import Halo
from bs4 import BeautifulSoup
from colorama import Style, Fore, init

MENSA_URL = "https://www.studierendenwerk-kaiserslautern.de/kaiserslautern" + \
            "/essen-und-trinken/tu-kaiserslautern/mensa/"

CACHE_EXT = '.mensacache'

spinner = Halo(spinner='line')

@contextmanager
def day_block():
    """Prints a day block in between two separator lines
    """
    print("="*40)
    try:
        yield
    finally:
        print("="*40 + Style.RESET_ALL)

# @Halo(text="Trying to load mensa-kl content from cache ...", spinner="line")
def get_page_from_cache(datestring):
    spinner.start('Trying to load mensa-kl content from cache ...')
    for file_cache in glob.glob('/tmp/*'+ CACHE_EXT):
        if file_cache == "/tmp/"+ datestring + CACHE_EXT:
            with open(file_cache, 'r') as page:
                content = page.read()
            spinner.stop_and_persist(symbol=Fore.GREEN+u"\u2713"+Fore.RESET, text="Found cached mensa-kl content!")
            return content
        else:
            os.remove(file_cache)
    spinner.stop_and_persist(symbol=Fore.RED+u"\u2717"+Fore.RESET, text="No cached mensa-kl content found!")
    return None

# @Halo(text="Trying to load mensa-kl content from web ...", spinner="line")
def get_page_from_web(datestring):
    spinner.start('Trying to load mensa-kl content from web ...')
    with urllib.request.urlopen(MENSA_URL) as response:
        if response.getcode() is not 200:
            spinner.stop_and_persist(symbol=Fore.RED+u"\u2717"+Fore.RESET, text="Error while loading mensa-kl webpage!")
            return None
        page = response.read()
    with open("/tmp/"+datestring+CACHE_EXT, 'w') as file_cache:
        file_cache.write(page.decode('utf-8'))
    spinner.stop_and_persist(symbol=Fore.GREEN+u"\u2713"+Fore.RESET, text="Successfully downloaded mensa-kl webpage!")
    return page

def get_mensakl_page():
    """Get the mensa page. The first request per boot and/or week
       is cached in /tmp to avoid repetitive requests.

    Returns:
        page contents, either served from a web request or from the
        cached file
    """

    datestring = datetime.today().strftime("%Y_%U")
    content = get_page_from_cache(datestring)
    if not content:
        return get_page_from_web(datestring)
    else:
        return content

def print_day(daily_content, is_today=False, vegetarian=False):
    """[summary]

    Arguments:
        daily_content -- HTML DOM of one day

    Keyword Arguments:
        is_today {bool} -- Whether or not the day in question is today (default: {False})
    """

    with day_block():
        print((Style.BRIGHT if is_today else "") + daily_content.h5.text + Style.RESET_ALL)
        rows = daily_content.findAll('div', {'class': 'subcolumns'})
        for row in rows:
            location = row.find('div', {'class': 'subcl'})
            foods = row.find('div', {'class': 'subcr'})
            foodlist = []
            for food in foods:
                try:
                    if food.text:
                        if re.findall(r',V,|\(V|V\)', food.text):
                            foodlist.append(Fore.GREEN + food.text + Fore.RESET)
                        elif not vegetarian:
                            foodlist.append(food.text)
                except AttributeError:
                    pass
            if foodlist:
                print('\t'.join([location.strong.text] + ['\n\t'.join(foodlist)]))

@click.command()
@click.option('--week', is_flag=True, help="List the food for the current week")
@click.option('--vegetarian', is_flag=True, help="Only list vegetarian options")
def mensa(week: bool = False, vegetarian: bool = False):
    """Query the webpage of the TUKL mensa and print the daily plans to the terminal
    """
    init()
    page = get_mensakl_page()
    if not page:
        print("ERROR: Could not find mensa kl page in cache, and couldn't" +
              "obtain page from web!")
        return
    page_soup = BeautifulSoup(page, "html.parser")
    for day in page_soup.findAll('div', {'class' : 'dailyplan_content'}):
        date_text = re.findall(r'\d+.\d+.\d+', day.h5.text)[0]
        date = datetime.strptime(date_text, '%d.%m.%Y')
        if date.date() == datetime.today().date():
            print_day(day, is_today=True, vegetarian=vegetarian)
        elif week:
            print_day(day, is_today=False, vegetarian=vegetarian)

if __name__ == '__main__':
    mensa()
