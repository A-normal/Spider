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
# 简繁切换标志，用于切换章节名称中的繁体汉字，默认为不切换(False)
opencc_tag = True

# 确保父目录存在
os.makedirs(save_dir, exist_ok=True)

# 视情况启用，实验发现由站点的访问限制，实际意义不大
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
# 针对特殊详情页，若无法运行可尝试启用
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
            r = session.get(url, verify=certifi.where())
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
                with closing(session.get(url, headers=download_header, stream=True, verify=certifi.        where())) as      response:
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
input('Press Enter To Colse……')
