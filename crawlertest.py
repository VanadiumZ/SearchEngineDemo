# modules import
import requests
from urllib.request import urljoin, urlparse
from url_normalize import url_normalize
from bs4 import BeautifulSoup
import time # add sleep
import random # consider adding random time of sleep
import os
import hashlib
from filter import val_url

def get_html(uri, headers={}, timeout=None, default_encoding=None):
    try:
        r = requests.get(uri, headers=headers, timeout=timeout)
        print(uri[:25], uri[-10:], r.status_code)
        r.raise_for_status
        if default_encoding:
            r.encoding = default_encoding
        return r.text
    except:
        return "000000"

def crawl_all_urls(html_doc, base_url):
    all_links = set()
    try:
        soup = BeautifulSoup(html_doc, 'html.parser')
    except:
        print("Fail to parse the html document!")
        return all_links
    
    for anchor in soup.find_all('a'):
        href = anchor.attrs.get('href')
        if (href != None and href != ""):  
            if not href.startswith('http'):
                href = urljoin(base_url, href)
            all_links.add(url_normalize(href))
    return all_links

def get_path(url, count):
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    path = url_hash + "_" + str(count) + ".html"
    return path

# ----------------------------------------------------------------------------
        
input_urls = ['http://ai.ruc.edu.cn/']
headers = {'user-agent': 'MyCrawler/2.0 (Windows NT 10.0; Win64; x64; en-US)'}
target = ["ai.ruc.edu.cn",
          "gsai.ruc.edu.cn",
          "www.jiqizhixin.com"]

# initialize the queue and control the urls picked
queue = []
all_urlset = set()
for url in input_urls:
    if url not in all_urlset:
        queue.append(url)
        all_urlset.add(url)

 
count = 0
used_urlset = set()
while (len(queue) > 0):
    # count += 1
    url = queue.pop(0)
    used_urlset.add(url)
    html_content = get_html(url, headers=headers, default_encoding='utf-8')
    url_sets = crawl_all_urls(html_content, url)

    # print(url_sets)
    for new_url in url_sets:
        if (new_url not in all_urlset) and (val_url(new_url, target)):
            queue.append(new_url)
            all_urlset.add(new_url)

    # save all the urls and corresponding html files
    # create the a new file named after the url
    # choose hash to name the htmlpath
    # and insert the url into the head of html file as an annotation

    if val_url(url, target):
        count += 1
        fold_path = "D:\Code\CodeTrainingGSAI\htmlsets_1"
        file_path = os.path.join(fold_path, get_path(url, count))
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"<!-- URL: {url} -->\n")
            f.write(html_content)
        print("done {}".format(count))

    wait_time = random.uniform(0, 0.5)
    if wait_time > 0:
       # print("wait for {}s and then crawl and scratch".format(wait_time))
        time.sleep(wait_time)
    


# print(all_urlset)






