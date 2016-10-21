import urllib.request
from bs4 import BeautifulSoup


response = urllib.request.urlopen('http://journals.aps.org/search/results?page=1&date=&sort=recent&per_page=20&start_date=&end_date=&clauses=%5B%7B%22operator%22:%22AND%22,%22field%22:%22all%22,%22value%22:%22skyrmion%22%7D%5D#title')
html = response.read()

soup = BeautifulSoup(html)

# Search for contents in the tags <script>...</script>
# From the APS results, the latest <script> is the one we need, which
# is called window.results = ...
results = soup.find_all('script')[-1]

# Now split the results. Every different result starts with
# an "action:" string, thus we separate the whole text by this pattern
# The 0th element is irrelevant, it contains the window.results string
results = results.text.split(r'{"actions":')[1:]

# Now we can regex the patterns
