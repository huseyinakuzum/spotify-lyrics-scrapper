from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re


class Scrapper:
    def __init__(self):
        pass

    def url_creator(self, artist, track):
        return 'https://www.azlyrics.com/lyrics/' + \
            re.sub(r'\W+', '', artist).lower().lstrip() + '/' +\
            re.sub(r'\W+', '', track).lower().lstrip()+'.html'

    def lyrics_extractor(self, url, aritst, track):
        page = urlopen(self.url_creator(aritst, track))
        soup = BeautifulSoup(page, 'html.parser')
        lyrics = str(soup).split('Sorry about that. -->')[-1].split('<!-- MxM')[0].replace('<br>', '').replace(
            '<br/>', '').replace('<i>', '').replace('</i>', '').replace('<div>', '').replace('</div>', '')
        return lyrics


quote_page = 'https://www.azlyrics.com/lyrics/arianagrande/makeup.html'


sc = Scrapper()

page = urlopen(sc.url_creator('Ariana Grande', 'MakeUp'))
soup = BeautifulSoup(page, 'html.parser')
print(str(soup).
      split('Sorry about that. -->')[-1].
      split('<!-- MxM')[0].
      replace('<br>', '').
      replace('<br/>', '').
      replace('<i>', '').
      replace('</i>', '').
      replace('<div>', '').
      replace('</div>', ''))
