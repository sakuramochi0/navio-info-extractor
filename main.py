from bs4 import BeautifulSoup
from glob import glob
import csv


def main():
    soups = get_soups()
    for soup in soups:
        items = create_items(soup)
        write_csv(items)


def get_soups():
    soups = []
    for filename in glob('html/*.html'):
        with open(filename) as f:
            soup = BeautifulSoup(f.read(), 'lxml')
            soups.append(soup)
    return soups


def create_items(soup):
    pass


def write_csv(items):
    pass


if __name__== '__main__':
    main()
