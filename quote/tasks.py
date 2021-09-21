from celery import shared_task
import sys

from bs4 import BeautifulSoup as b_s

import requests

from quote.models import Author, Quote

SITE = 'https://quotes.toscrape.com'

page = 1
nomer = 0


@shared_task
def quote_task():
    global page
    global nomer

    try:
        r = requests.get(SITE)
        if r.status_code != requests.codes.ok:
            return
        sys.stdout.write(f"{SITE} status is {r.status_code}")

        for _ in range(5):
            URL = f'{SITE}/page/{page}'
            r = requests.get(URL)
            soup = b_s(r.text, 'html.parser')
            check = soup('div', {'class': 'row'})[1]
            if 'No quotes found!' in check.find('div', {'class': 'col-md-8'}).get_text():
                sys.stdout.write('It`s all')
                return
            try:
                all_quote = soup('div', {'class': 'quote'})[nomer]
                print()
                print('--------------------------------------------------------------')
                quote_text = all_quote.find('span', {'class': 'text'}).get_text()
                print(quote_text)
                quote_author = all_quote.find('small').get_text()
                print(quote_author)

                obj, created = Author.objects.get_or_create(name=quote_author)
                if not created:
                    a_id = Author.objects.get(name=obj).id
                else:
                    a_id = Author.objects.values_list('id', flat=True).last()

                Quote.objects.get_or_create(quote=quote_text, author_id=int(a_id))
                nomer += 1
                print(f'page {page}-{nomer}')
            except:
                nomer = 0
                page += 1

    except:
        raise Exception('Smth wrong :(')

