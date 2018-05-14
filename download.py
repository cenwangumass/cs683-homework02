import json
import re

import requests
from bs4 import BeautifulSoup


def main():
    base_url = 'http://rbr.cs.umass.edu/shlomo/classes/683/source/'
    homework_url = base_url + 'hw2.html'
    authentication = ('683', 'deepAI')

    response = requests.get(homework_url, auth=authentication)
    html = BeautifulSoup(response.text)
    pattern = re.compile(r'sudoku/puz-(\d+).txt')
    sudokus = {}
    for a_element in html.find_all('a', href=pattern):
        link = a_element['href']
        number = pattern.match(link).group(1)
        response = requests.get(base_url + link, auth=authentication)
        sudokus[number] = response.text

    with open('sudokus.json', 'w') as f:
        json.dump(sudokus, f)


if __name__ == '__main__':
    main()
