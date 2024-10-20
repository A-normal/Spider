import requests
import os
from bs4 import BeautifulSoup
from contextlib import closing
from tqdm import tqdm
import time
import certifi

"""
    Author:
        A-normal
"""

# 创建保存目录，请添加漫画名称
# eg: D:/IDMLibrary/Comic/我在异界当乞丐
save_dir = 'D:/'

# 由于部分情况获取的仅为相对链接，须补齐完整链接
pre_url = "https://www.baozimh.com"
# 目标url，仅支持单部漫画，即链接为漫画主页链接
target_url = "https://www.baozimh.com/comic/wozaiyijiedangqigai-wrectage"
# 章节间请求延迟（秒）
delay = 2
# 最大重试次数
max_retries = 5  
# 每次重试的延迟（秒）
retry_delay = 2  

# 确保父目录存在
os.makedirs(save_dir, exist_ok=True)

# 获取动漫章节链接和章节名
r = requests.get(url = target_url , verify=certifi.where())
bs = BeautifulSoup(r.text, 'lxml')

divs = bs.find_all('div', class_='l-box')

# 获取第二个 div
if len(divs) > 1:
    div = divs[1]

list_url = div.find_all('a')
list_name = div.find_all('span')
names = []
urls = []

for a in list_url:
    href = a.get('href')
    urls.insert(0, pre_url+href)

num = 1

for span in list_name:
    text = span.text.strip()
    # 由于漫画章节名称含有非法字符字符，应替换，其他非法字符请个人添加，但不要提交pull
    text = text.replace('/','or')
    text = text.replace('?','')
    names.insert(0, "第" + str(num) + "章" + text)
    num+=1

# 下载漫画 
for i, url in enumerate(tqdm(urls)):
    # 简单的反爬措施，指定链接来源
    download_header = {
        'Referer': url
    }
    name = names[i]
    chapter_save_dir = os.path.join(save_dir, name)

    # 检查并创建章节保存目录，若目录已存在则跳过此章节下载
    # 该处逻辑可优化
    if not os.path.exists(chapter_save_dir):
        os.mkdir(chapter_save_dir)
    else : continue

    # 尝试获取章节
    for attempt in range(max_retries):
        try:
            r = requests.get(url, verify=certifi.where())
            break
        except requests.exceptions.RequestException as e:
            print(f"请求链接失败: {e}, 正在重试... (尝试次数: {attempt + 1})")
            time.sleep(retry_delay)  # 暂停一段时间后重试


    html = BeautifulSoup(r.text, 'lxml')
    pics = html.find_all('img')

    # 下载章节图片
    for idx, pic in enumerate(pics):
        pic_name = '%03d.jpg' % (idx + 1)
        pic_save_path = os.path.join(chapter_save_dir,pic_name)
        url = pic.get('src')

        # 尝试下载图片
        for attempt in range(max_retries):
            try:
                with closing(requests.get(url, headers=download_header, stream=True, verify=certifi.        where())) as      response:
                    if response.status_code == 200:
                        with open(pic_save_path, "wb") as file:
                            for data in response.iter_content(chunk_size=1024):
                                file.write(data)
                        # 成功后退出循环
                        break 
            except requests.exceptions.RequestException as e:
                print(f"请求图片失败: {e}, 正在重试... (尝试次数: {attempt + 1})")
                time.sleep(retry_delay)  # 暂停一段时间后重试
    time.sleep(delay)