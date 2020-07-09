from bs4 import BeautifulSoup
import argparse
import pandas as pd
from typing import Dict, List, Iterator


def main(args):
    soups = get_soups(args.html_files)
    items_set = []
    for soup in soups:
        items_set.append(create_items(soup))
    write_csv(args.csv_path, items_set)


def get_soups(filenames: [str]) -> List[BeautifulSoup]:
    """html ディレクトリに保存しておいた html を読み込んで、BeautifulSoup オブジェクトのリストに変換する。"""
    soups = []
    for filename in filenames:
        with open(filename) as f:
            soup = BeautifulSoup(f.read(), 'lxml')
            soups.append(soup)
    return soups


def create_items(soup: BeautifulSoup) -> Iterator[Dict[str, str]]:
    """1ページ分の BeautifulSoup オブジェクトを受け取り、サークルデータを抽出してリストを作る。"""
    items = soup.select('.circle_list_item')
    items = map(convert_item, items)
    return items


def convert_item(item: BeautifulSoup) -> Dict[str, str]:
    """1サークル分の BeautifulSoup オブジェクトを受け取って、保存するデータを抽出する。"""
    new = {
        'id': item.select('input.CircleId')[0]['value'],
        'circle_space': item.select('.CircleSpace')[0].text,  # .CurrentCheckColor
        'work': item.select('.ArtifactTitle')[0].text,
        'cp': item.select('.ArtifactTendency')[0].text,
        'circle_name_kana': item.select('.CircleNameKana')[0].text,
        'circle_name': item.select('.CircleName')[0].text,
        'pen_name': item.select('.CirclePenname')[0].text,
        'manga': item.select('.CircleIsManga')[0].text,
        'novel': item.select('.CircleIsNovel')[0].text,
        'r18': item.select('.CircleR18')[0].text,
        'circle_cut_url': item.select('.CircleCut')[0]['src'],
        'twitter_url': item.select('.icon-twitter')[0].parent['href'],
        'website_url': item.select('.icon-homepage')[0].parent['href'],
        'pixiv_url': item.select('.icon-pixiv')[0].parent['href'],
    }
    return new


def write_csv(csv_path, items_set: List[List[Dict[str, str]]]):
    """アイテムセットを panndas.DataFrame に変換して csv 形式で保存する。"""
    header = (
        'id',
        'circle_space',
        'work',
        'cp',
        'circle_name_kana',
        'circle_name',
        'pen_name',
        'manga',
        'novel',
        'r18',
        'circle_cut_url',
        'twitter_url',
        'website_url',
        'pixiv_url',
    )
    df = pd.DataFrame(columns=header)
    for items in items_set:
        for item in items:
            # append row
            df.loc[df.shape[0]] = item

    with open(csv_path, 'w') as f:
        f.write(df.to_csv(index=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path')
    parser.add_argument('html_files', nargs='+')
    args = parser.parse_args()
    main(args)
