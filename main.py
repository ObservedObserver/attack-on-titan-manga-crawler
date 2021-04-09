# -*- coding: UTF-8 -*-
import requests as req
from bs4 import BeautifulSoup
import re
import time
import os

host_path = 'https://p5.manhuapan.com'
start_chepter_num = 126
end_chepter_num = 138
base_folder = './attack-on-titan'


def get_page_soup(chepter_num, page_num):
    res = req.get('https://manhua.fzdm.com/39/%d/index_%d.html' % (chepter_num, page_num))
    print('https://manhua.fzdm.com/39/%d/index_%d.html' % (chepter_num, page_num), res)
    html_text = res.text
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup


def is_page_end(soup, current_page_num):
    nav = soup.select('.navigation')
    max_page_number = 0
    if len(nav) > 0:
        page_list = nav[0].select('a')
        for page in page_list:
            page_file_name = page['href']
            page_num_matches = re.search(r'index_([0-9]+)\.html', page_file_name)
            if page_num_matches is not None:
                page_num = int(page_num_matches.group(1))
                max_page_number = max(max_page_number, page_num)
    return max_page_number <= current_page_num


def get_image_url(soup):
    scripts = soup.find_all('script')
    img_url = ''
    for script in scripts:
        # print(script.string)
        content_text = script.string
        if content_text is not None:
            # print(content_text)
            path = re.search(r'var mhurl\s?=\s?\"(.+?)\";', content_text)
            if path is not None:
                img_path = path.group(1)
                img_url = host_path + '/' + img_path
                return img_url
    return img_url


def download_image(img_url, img_name):
    img = req.get(img_url)
    with open(img_name, 'wb') as f:
        f.write(img.content)


def create_chepter_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


if __name__ == '__main__':
    for chepter_num in range(start_chepter_num, end_chepter_num + 1):
        folder_path = base_folder + '/' + str(chepter_num)
        create_chepter_folder_if_not_exists(folder_path)
        page_num = 0
        is_end = False
        while not is_end:
            soup = get_page_soup(chepter_num, page_num)
            is_end = is_page_end(soup, page_num)
            img_url = get_image_url(soup)
            print('imgurl=', img_url, is_end)
            if img_url != '':
                download_image(img_url, folder_path + '/' + str(page_num) + '.jpg')
            time.sleep(0.2)
            page_num += 1


