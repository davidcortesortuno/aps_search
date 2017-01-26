import urllib.request
from bs4 import BeautifulSoup
import json
import argparse
import re
import textwrap as tw

NWRAP = 68

parser = argparse.ArgumentParser(description='PRB Journal Search')

parser.add_argument('-kw', '--keyword', help='Search keyword',
                    default='skyrmion')

# Parser arguments
args = parser.parse_args()


# -----------------------------------------------------------------------------

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# -----------------------------------------------------------------------------

class APSSearch(object):

    def __init__(self, keyword, pages, n_results=10):

        self.url = ('http://journals.aps.org/search/'
                    'results?page=2&date=&sort=recent&per_page=20'
                    '&start_date=&end_date=&clauses=%5B%7B%22operator%22:'
                    '%22AND%22,%22field%22:%22all%22,%22value%22:'
                    '%22{0}%22%7D%5D#title').format(args.keyword)

    def get_results(self):
        response = urllib.request.urlopen(self.url)
        html = response.read()

        soup = BeautifulSoup(html, "lxml")

        # Search for contents in the tags <script>...</script>
        # From the APS results, the latest <script> is the one we need, which
        # is called window.results = ...
        self.results = soup.find_all('script')[-1]

        # Now split the results. Every different result starts with
        # an "action:" string, thus we separate the whole text by this pattern
        # The 0th element is irrelevant, it contains the window.results string
        results = results.text.split(r'{"actions":')[1:]
        results[-1] = results[-1].split('"facets"')[0][:-2]
        results = [r'{"actions":' + r.rstrip(',') for r in results]

        results = [json.loads(r) for r in results]

    def print_results(self):
        for r in results:
            r['title'] = re.sub(r'<[^>]*>', '', r['title'])
            r['title'] = bcolors.BOLD + r['title'] + bcolors.ENDC
            r['title'] = tw.fill(r['title'], NWRAP).replace('\n', '\n' + ' ' * 13)

            r['authors'] = tw.fill(r['authors'], NWRAP).replace('\n', '\n' + ' ' * 13)

        for r in results:
            print('{:<21} {:<}'.format(bcolors.OKBLUE + r['date'] + bcolors.ENDC,
                                       r['title']))
            print('{:<12} {:<}'.format('', r['authors']))
            print('{:<12} {:<}'.format('', bcolors.OKGREEN + r['journal'] + bcolors.ENDC))
            print('{:<12} {:<}'.format('',
                                       'http://journals.aps.org/' +
                                       r['actions']['pdf']['link']
                                       )
                  )
            print('-' * 80)
