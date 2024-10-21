import requests
import os
from bs4 import BeautifulSoup
from contextlib import closing
from tqdm import tqdm
import time
import certifi
import opencc

"""
    Author:
        A-normal
"""

# 创建保存目录，请添加漫画名称
# eg: D:/IDMLibrary/Comic/我在异界当乞丐
save_dir = 'D:/IDMLibrary/Comic/女子学院的男生'

# 由于部分情况获取的仅为相对链接，须补齐完整链接
pre_url = "https://www.baozimh.com"
# 目标url，仅支持单部漫画，即链接为漫画主页链接
target_url = "https://www.baozimh.com/comic/nuzixueyuandenansheng-hongdaomanhua"
# 章节间请求延迟（秒）
delay = 2
# 最大重试次数
max_retries = 5  
# 每次重试的延迟（秒）
retry_delay = 2  
opencc_tag = True

# 确保父目录存在
os.makedirs(save_dir, exist_ok=True)

# 视情况启用
# 使用Session模拟Cookie
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
session = requests.Session()

# 获取动漫章节链接和章节名
r = session.get(target_url , headers= headers )
bs = BeautifulSoup(r.text, 'lxml')

divs = bs.find_all('div', class_='l-box')

# 获取第二个 div
if len(divs) > 1:
    div = divs[1]
# else :
    # div = divs

list_url = div.find_all('a')
list_name = div.find_all('span')
names = []
urls = []

for a in list_url:
    href = a.get('href')
    urls.insert(0, pre_url+href)

# 两个章节名称指标，tag用于指示时候获取到的章节是否含有章节数，num用于记录当前章节数（由于漫画默认排序方式问题，索引可能不靠谱）
name_tag = False
num = 1
str = ['0','1','2','3','4','5','6','7','8','9','I','V','X']
if opencc_tag :
    convert = opencc.OpenCC('t2s')

for span in list_name:
    text = span.text.strip()
    # 简繁切换
    if opencc_tag :
        text = convert.convert(text)
    # 由于漫画章节名称含有非法字符字符，应替换，其他非法字符请个人添加，但不要提交pull
    text = text.replace('/','or')
    text = text.replace('?','')
    # 检测漫画名称是否含有章节数（包括数字和罗马字母）
    if not name_tag :
        i = 0
        while i<len(str) :
            if str[i] in text : 
                name_tag = True
                break
            i+=1
    if not name_tag : 
        names.insert(0, "第" + str(num) + "章" + text)
        num+=1
    else : 
        names.insert(0, text)