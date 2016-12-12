import urllib.request
from bs4 import BeautifulSoup
import json
import argparse
import re

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

# -----------------------------------------------------------------------------

url = ('http://journals.aps.org/search/'
       'results?page=1&date=&sort=recent&per_page=20'
       '&start_date=&end_date=&clauses=%5B%7B%22operator%22:'
       '%22AND%22,%22field%22:%22all%22,%22value%22:'
       '%22{0}%22%7D%5D#title').format(args.keyword)

response = urllib.request.urlopen(url)
html = response.read()

soup = BeautifulSoup(html, "lxml")

# Search for contents in the tags <script>...</script>
# From the APS results, the latest <script> is the one we need, which
# is called window.results = ...
results = soup.find_all('script')[-1]

# Now split the results. Every different result starts with
# an "action:" string, thus we separate the whole text by this pattern
# The 0th element is irrelevant, it contains the window.results string
results = results.text.split(r'{"actions":')[1:]
results[-1] = results[-1].split('"facets"')[0][:-2]
results = [r'{"actions":' + r.rstrip(',') for r in results]

results = [json.loads(r) for r in results]

for r in results:
    r['title'] = re.sub(r'<[^>]*>', '', r['title'])

for r in results:
    print('{:<11} {:<}'.format(bcolors.OKBLUE + r['date'] + bcolors.ENDC,
                               r['title']))
    print('{:<11} {:<}'.format('', r['authors']))
    print('{:<11} {:<}'.format('', bcolors.OKGREEN + r['journal'] + bcolors.ENDC))
    print('{:<11} {:<}'.format('',
                               'http://journals.aps.org/' +
                               r['actions']['pdf']['link']
                               )
          )
    print('-' * 80)
