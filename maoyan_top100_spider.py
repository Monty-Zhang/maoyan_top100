'''
    Author:Monty
    Date:2019-06-06
    Function:Using re to scrape top100 films from maoyan film
    version:1.0
'''

import requests
import re
import csv


def getHTML(url):
    '''获得目标url的响应体'''
    try:
        headers = {'User-Agent':'Mozilla'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except:
        print('响应失败')

def parseHTML(html):
    '''使用正则解析HTML'''
    pattern = re.compile(r'<dd>.*?>(.*?)</i>.*?<a\s+href="(.*?)" title="(.*?)".*?"star">(.*?)</p>.*?"releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',re.S)
    film_lst = pattern.findall(html)
    if film_lst:
        return film_lst
    else:
        print('解析失败')

def info_to_dict(info):
    '''把电影信息整理成字典'''
    film_info = {}
    film_info['rank'] = info[0]
    film_info['url'] = 'http://maoyan.com' + info[1]
    film_info['title'] = info[2]
    film_info['star'] = info[3].strip()[3:]
    film_info['releasetime'] = info[4][5:]
    film_info['score'] = info[5] + info[6]
    return film_info


def main():
    # 设置newline=''不会出现两行之间空一行
    with open('./Download/maoyanTOP100.csv', 'a', newline='', encoding='utf-8') as csvFile:
        filednames = ['rank', 'url', 'title', 'star', 'releasetime', 'score']
        writer = csv.DictWriter(csvFile, fieldnames=filednames)
        # 这步很重要，不然没有表头
        writer.writeheader()

        for page in range(10):
            url = 'https://maoyan.com/board/4?offset={}'.format(10*page)
            html = getHTML(url)
            film_info_lst = parseHTML(html)

            for film in film_info_lst:
                film_info = info_to_dict(film)
                writer.writerow(film_info)

    print('Scraping finished')


if __name__ == '__main__':
    main()
