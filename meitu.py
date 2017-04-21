# -*- coding: utf-8 -*-
import re
import os
import sys
import urllib2
import requests
from lxml import etree
from bs4 import BeautifulSoup

# # 输入字符串,并匹配A-Z a-z，错误则结束程序
# file_path = raw_input("Please enter the directory path to save,like D or E\n")
# if re.search('[A-Za-z]', file_path) is None:
#     print '输入路径错误'
#     # 结束程序
#     sys.exit()
# else:
#     print ''
#
# # 在路径处创建spider文件夹
# if os.path.exists(file_path+':\\spider') is False:
#     os.mkdir(file_path+':\\spider')
#     print 'spider' + '文件夹已创建,文件正在准备下载'
# else:
#     print '文件夹已存在,文件正在准备下载'


# 文件夹定位
os.chdir('D:\\spider')
# 网页特征数
_id_ = input('please input id\n')
items = _id_
# 入口url
url = 'http://www.meitulu.com/item/%s.html' % items

# 自定义header
send_headers = {
    'Host': 'www.meitulu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
                  'Safari/537.36',
    'Accept': 'ttext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive'
}

# xpath方式获取text
# page_url = requests.get(url).content
# s = etree.HTML(page_url)
# page_list = s.xpath('/html/body/center/div[1]/a[11]/text()')
# pages = int(page_list[0])
# print pages

# 确定页码
page_url = requests.get(url).content
page_soup = BeautifulSoup(page_url, 'lxml')
page_soups = page_soup.find_all('a', {'href': re.compile(r'http://www.meitulu.com/item/\d+_\d')})
add_lists = []
for i in page_soups:
    pic_address = i.get('href')
    add_lists.append(pic_address)
page_strings = add_lists[-2]
page_string = page_strings[-7:-5]
# 替换特殊符号
pages_ = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。<>？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"), page_string)

# 网页数
print pages_
pages = int(pages_)
nums = pages

# 保存的图片地址文件名
fp_name = 'address.txt'
a = BeautifulSoup(urllib2.urlopen(url).read(), 'lxml', from_encoding='utf-8').h1.text
__id = str(_id_)
file_names = 'D:\\spider\\' + __id + '.' + a

# 替换特殊符号
real_name = re.sub("[\s+\!\/_,$%^*(+\"\']+|[+——！，。<>？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"), file_names)
print(real_name)

# 文件保存位置
os.mkdir(real_name)
os.chdir(real_name)


# 获取第一个网页图片
def get_first_address():
    url_1 = 'http://www.meitulu.com/item/%s.html' % items
    response = urllib2.Request(url_1, headers=send_headers)
    responses = urllib2.urlopen(response)
    soup = BeautifulSoup(responses.read(), 'lxml', from_encoding='utf-8')
    soups = soup.find_all('img', {'src': re.compile(r'http://pic.yiipic.com/uploadfile/\d{4}/\d{4}/\d*.jpg')})
    address_list = []

    for j in soups:
        pic_address = j.get('src')
        address_list.append(pic_address)
# 图片地址写入picture.txt文件里
        fp = open(fp_name, 'a+')
        ir = requests.get(pic_address, stream=True)
        name = pic_address.split('/')[6]
        if ir.status_code == 200:
            with open(name, 'wb') as f:
                for chunk in ir:
                    f.write(chunk)
        fp.write(pic_address + '\n')
    print 'Downloading'
    print address_list


# 获取剩余网页图片
def get_remaining_address():
    url_2 = 'http://www.meitulu.com/item/%s_%s.html' % (items, x)
    # print url_2
    response = urllib2.Request(url_2, headers=send_headers)
    responses = urllib2.urlopen(response)
    soup = BeautifulSoup(responses.read(), 'lxml', from_encoding='utf-8')
    soups = soup.find_all('img', {'src': re.compile(r'http://pic.yiipic.com/uploadfile/\d{4}/\d{4}/\d*.jpg')})
    address_list = []

    for k in soups:
        pic_address = k.get('src')
        address_list.append(pic_address)
# 图片地址写入picture.txt文件里
        fp = open(fp_name, 'a+')
# 下载图片
        ir = requests.get(pic_address, stream=True)
        name = pic_address.split('/')[6]
        if ir.status_code == 200:
            with open(name, 'wb') as f:
                for chunk in ir:
                    f.write(chunk)

        fp.write(pic_address + '\n')
    print 'Downloading'
    print address_list

# 获取全部网页图片
get_first_address()
for x in range(2, nums+1):
    get_remaining_address()

print 'Download finished'
