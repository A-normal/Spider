import requests
import os
import time
import certifi
from urllib import response
from contextlib import closing
from bs4 import BeautifulSoup


url = "https://www.czmanga.com/comic/chapter/wozaiyijiedangqigai-wrectage/0_224.html"

r = requests.get(url , verify=certifi.where())

html = BeautifulSoup(r.text, 'lxml')
# script_info = html.script
pics = html.find_all('img')

# print(pics)

urls = []

for i,item in enumerate(pics):
    urls.insert(0,item.get('src'))


print(urls)

# print(enumerate(pics))
# pics = sorted(pics, key=lambda x:int(x))
# for idx, pic in enumerate(pics):
#     pic_name = '%03d.jpg' % (idx + 1)
#     pic_save_path = os.path.join("chapter_save_dir", pic_name)
#     url = pic.get('src')
#     print(url)  
#     with closing(requests.get(url, stream = True , verify=False)) as response:  
#         chunk_size = 1024  
#         # print(response)
#         # 这儿看到response什么也没有，仅包含状态码，故删除context-length
#         # content_size = int(response.headers['content-length'])  
#         if response.status_code == 200:
#             with open(pic_save_path, "wb") as file:  
#                 for data in response.iter_content(chunk_size=chunk_size):  
#                     file.write(data)  
#         else:
#             print('链接异常')
# time.sleep(10)