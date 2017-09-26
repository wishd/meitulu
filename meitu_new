# coding:utf8
import requests
import os
import re
from bs4 import BeautifulSoup

# eigenvalues of website
_id_ = input('please input a number\n')
items = _id_

# Directory path
dir_name = '/home/wishd/meitulu/%s' % items
os.mkdir(dir_name)
os.chdir(dir_name)
# Entry url
entry_url = 'https://www.meitulu.com/item/%s.html' % items
# Pictures address list
pic_add_list = []
# Websites address list
web_add_list = []
# Fake headers
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 '
                         'Safari/537.36',
           'Accept': 'ttext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Connection': 'keep-alive'}


# get the page number
def page_number():
    web_add_list.append(entry_url)
    response = requests.get(entry_url, headers=headers).content
    soup = BeautifulSoup(response, 'lxml')
    soups = soup.find_all('a', {'href': re.compile(r'/item/\d+_\d+.html')})
    page_numbers = soups[-2].text
    for i in range(2, int(page_numbers)+1):
        url = 'https://www.meitulu.com/item/%s_%s.html' % (items, i)
        web_add_list.append(url)


# get address of pictures
def pic_address():
    print u'正在获取图片地址...'
    page_number()
    # print web_add_list
    for urls in web_add_list:
        response = requests.get(urls, headers=headers).content
        soup = BeautifulSoup(response, 'lxml')
        soups = soup.find_all('img', {'src': re.compile(r'http://mtl.ttsqgs.com/images/img/\d+/\d+.jpg')})
        # print soups[0:-8]
        for i in soups[0:-8]:
            add = i.get('src')
            pic_add_list.append(add)
    print pic_add_list
    print u'图片地址获取完成'


# download the pictures
def pic_download():
    print u'开始下载图片...'
    for pic in pic_add_list:
        ir = requests.get(pic, stream=True)
        name = pic.split('/')[6]
        if ir.status_code == 200:
            with open(name, 'wb') as f:
                for chunk in ir:
                    f.write(chunk)
    print u'图片下载完成'


if __name__ == '__main__':
    pic_address()
    pic_download()
