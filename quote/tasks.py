from celery import shared_task
import sys

from bs4 import BeautifulSoup as b_s

import requests
from django.core.mail import send_mail

from quote.models import Author, Quote

SITE = 'https://quotes.toscrape.com'


@shared_task
def quote_task():
    page = 1
    nomer = 0

    try:
        r = requests.get(SITE)
        if r.status_code != requests.codes.ok:
            return
        sys.stdout.write(f"{SITE} status is {r.status_code}")
        kol_vo = 0
        while True:
            URL = f'{SITE}/page/{page}'
            r = requests.get(URL)
            soup = b_s(r.text, 'html.parser')
            check = soup('div', {'class': 'row'})[1]
            if 'No quotes found!' in check.find('div', {'class': 'col-md-8'}).get_text():
                sys.stdout.write('It`s all')
                send_mail('Quotes', 'No quotes found!', 'admin@mail.com', ['olya@gmail.com'])
                return
            all_quote = soup('div', {'class': 'quote'})[nomer]
            # print(nomer+1)
            # print('--------------------------------------------------------------')
            quote_text = all_quote.find('span', {'class': 'text'}).get_text()
            #print(quote_text)
            quote_author = all_quote.find('small').get_text()
            #print(quote_author)
            quote_author_about = all_quote.find('a').get('href')
            #print(quote_author_about)

            obj, created = Author.objects.get_or_create(name=quote_author, about=quote_author_about)

            obj1, created1 = Quote.objects.get_or_create(quote=quote_text, author=obj)
            if created1:
                kol_vo += 1
                #print(f'page {page}-{nomer+1}')
            nomer += 1

            if nomer == 10:
                nomer = 0
                page += 1
            if kol_vo == 5:
                break

    except:
        raise Exception('Smth wrong :(')
