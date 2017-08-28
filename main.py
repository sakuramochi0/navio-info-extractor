from bs4 import BeautifulSoup
from glob import glob
import pandas as pd
import csv


def main():
    soups = get_soups()
    items_set = []
    for soup in soups:
        items_set.append(create_items(soup))
    write_csv(items_set)


def get_soups():
    '''html ディレクトリに保存しておいた html を読み込んで、BeautifulSoup オブジェクトのリストに変換する。'''
    soups = []
    for filename in glob('html/*.html'):
        with open(filename) as f:
            soup = BeautifulSoup(f.read(), 'lxml')
            soups.append(soup)
    return soups


def create_items(soup):
    '''1ページ分の BeautifulSoup オブジェクトを受け取り、サークルデータを抽出してリストを作る。'''
    items = soup.select('.circle_list_item')
    items = map(convert_item, items)
    return items


def convert_item(item):
    '''1サークル分の BeautifulSoup オブジェクトを受け取って、保存するデータを抽出する。'''
    new = {}
    new['id'] = item.select('input.CircleId')[0]['value']
    new['circle_space'] = item.select('.CircleSpace')[0].text
    new['work'] = item.select('.ArtifactTitle')[0].text
    new['cp'] = item.select('.ArtifactTendency')[0].text
    new['circle_name_kana'] = item.select('.CircleNameKana')[0].text
    new['circle_name'] = item.select('.CircleName')[0].text
    new['penname'] = item.select('.CirclePenname')[0].text
    new['manga'] = item.select('.CircleIsManga')[0].text
    new['novel'] = item.select('.CircleIsNovel')[0].text
    new['r18'] = item.select('.CircleR18')[0].text
    new['circle_cut'] = item.select('.CircleCut')[0]['src']
    new['twitter'] = item.select('.icon-twitter')[0].parent['href']
    new['website'] = item.select('.icon-homepage')[0].parent['href']
    new['pixiv'] = item.select('.icon-pixiv')[0].parent['href']
    return new


def write_csv(items_set):
    '''アイテムセットを panndas.DataFrame に変換して csv 形式で保存する。'''
    header = (
        'id',
        'circle_space',
        'work',
        'cp',
        'circle_name_kana',
        'circle_name',
        'penname',
        'manga',
        'novel',
        'r18',
        'circle_cut',
        'twitter',
        'website',
        'pixiv',
    )
    df = pd.DataFrame(columns=header)
    for items in items_set:
        for item in items:
            # append row
            df.loc[df.shape[0]] = item

    with open('circles.csv', 'w') as f:
        f.write(df.to_csv(index=False))


if __name__== '__main__':
    main()
