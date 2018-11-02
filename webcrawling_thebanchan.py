import requests
import pandas as pd
import re
from collections import OrderedDict, Counter
from bs4 import BeautifulSoup

def get_food_information(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    information = soup.find('div', {'class': 'gds_tbl'})
    keys = [x.text for x in table.table.findAll('th', {'scope': 'row'})]
    values = [x.text for x in table.table.findAll('td')]
    res = dict(zip(keys, values))
    return res
