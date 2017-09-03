# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 14:58:49 2017

@author: adolph
"""
import pymongo
from bs4 import BeautifulSoup
import progressbar
from requests.exceptions import RequestException
import requests
import json
import os
import sys

#url ="http://www.ximalaya.com/32423029/album/4078852/"
#url = "http://www.ximalaya.com/4228109/album/220570"
#url = 'http://www.ximalaya.com/10936615/album/7651313/'
#        "http://www.ximalaya.com/4228109/album/4291180/",#鲁迅
#        "http://www.ximalaya.com/4228109/album/222251/",#左传-原文朗读【十三经】
#        "http://www.ximalaya.com/4228109/album/256969/",#吕氏春秋（原文朗读）
#        "http://www.ximalaya.com/4228109/album/227814/",#管子-原文朗读
#        "http://www.ximalaya.com/4228109/album/268522/",#三国演义-原文朗读【四大名著
#        "http://www.ximalaya.com/4228109/album/232270/", #儒林外史
#        "http://www.ximalaya.com/4228109/album/4030672/",#桃花扇-原文朗读
#        "http://www.ximalaya.com/4228109/album/221374/",#庄子（原文朗读）
#        "http://www.ximalaya.com/4228109/album/221871/",#韩非子（原文朗读）
#        "http://www.ximalaya.com/4228109/album/274668/",#后汉书-原文朗读【前四史】
#        "http://www.ximalaya.com/4228109/album/220518/",#资治通鉴》（原文朗读）
#        "http://www.ximalaya.com/4228109/album/220568/",#汉书-原文朗读【前四史】
#        "http://www.ximalaya.com/4228109/album/223022/",#荀子-原文朗读



urls=[
#        "http://www.ximalaya.com/2966909/album/3929799",#传习录.王阳明-心学
#        "http://www.ximalaya.com/1770109/album/9697557/",#论语
#        "http://www.ximalaya.com/1770109/album/6398825/",#全本《孟子》原文（名家诵读欣赏）
#        "http://www.ximalaya.com/1770109/album/6189759/",#全本《孟子》精读
        "http://www.ximalaya.com/1770109/album/9460967",#精一之道——全本王阳明《传习录》全译（独家授权）
        "http://www.ximalaya.com/album/4605839",#诗经里的哀乐
        "http://www.ximalaya.com/35071918/album/5486477/",#儒家修身九讲
        "http://www.ximalaya.com/35071918/album/5511418/",#论语——温润心灵"
        "http://www.ximalaya.com/35071918/album/6632753/",#中国的智慧 韦政通著
        "http://www.ximalaya.com/35071918/album/8788061/",#道家的处世智慧 葛荣晋
        "http://www.ximalaya.com/13127766/album/2713249",#阿含经的故事
        "http://www.ximalaya.com/32423029/album/3003147",#问中医几度秋凉
        "http://www.ximalaya.com/60979533/album/6610854",#《钱穆《阳明学述要》》
        "http://www.ximalaya.com/4228109/album/222427/",#四书（大学_中庸_论语_孟子）【十三

    ]




headers = {
"Host":"www.ximalaya.com",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
"Accept":"application/json, text/javascript, */*; q=0.01",
"Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
"Accept-Encoding":"gzip, deflate, br",
"Referer":"http://www.ximalaya.com",
"X-Requested-With":"XMLHttpRequest",
"Connection":"keep-alive"
}


def download_audio(audio_url,audio_path,num):
    if num==0:
        print(audio_path+"实在没救了，放弃吧！\n")
        return 
    
    if os.path.exists(audio_path+'.m4a'):
        print(audio_path+"存在，将跳过\n")
        return 
    try:
        response = requests.get(audio_url, stream=True)     
        total_length = int(response.headers.get("Content-Length"))
    except:
        print("下载"+audio_path+"出错，再试一次\n")
        download_audio(audio_url,audio_path,num-1)
        return
    with open(audio_path+'.m4a', 'wb') as f:
        chunks = 0
        sys.stdout.flush()
        print("\n"+audio_path+":\n")
        sys.stdout.flush()
        widgets = ["", progressbar.Percentage(), ' ',
                   progressbar.Bar(marker='#', left='[', right=']'),
                   ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
        pbar = progressbar.ProgressBar(widgets=widgets, maxval=total_length).start()
        for chunk in response.iter_content(chunk_size=256):
            if chunk:
                f.write(chunk)
                f.flush()
                chunks += len(chunk)
            pbar.update(chunks)
        pbar.finish()
        

def download_one_page(Soup):
    totle_li = Soup.find('div',class_='album_soundlist ').find_all('li')
    for li in totle_li:
        json_url = "http://www.ximalaya.com/tracks/"+str(li["sound_id"])+'.json'
        json_content = requests.get(json_url,headers = headers)
        data = json.loads(json_content.text)
        tittle = data["title"]
        audio_url = data["play_path"]
        download_audio(audio_url,tittle,3)
    


def parse_index_page(index_url,num):
    if num ==0:
        print(index_url+"行不通，将放弃\n")
        return
    try:
        response = requests.get(index_url,headers = headers)
    except:
        print(index_url+"没反映，将再试一次\n")
        parse_index_page(index_url,num-1)
        return
    Soup = BeautifulSoup(response.text,'lxml')
    dirname = Soup.title.string
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    os.chdir(dirname)
    download_one_page(Soup)
    page_indexs=Soup.find('div',class_='pagingBar_wrapper')
    if page_indexs is not None:
        for i in range(2,len(page_indexs.find_all("a"))):
            parse_page_url = index_url+"?page="+str(i)
            try :
                response = requests.get(parse_page_url,headers = headers)
                Soup = BeautifulSoup(response.text,'lxml')
                download_one_page(Soup)
            except :
                try :
                    response = requests.get(parse_page_url,headers = headers)
                    Soup = BeautifulSoup(response.text,'lxml')
                    download_one_page(Soup)
                except:
                    print(parse_page_url+"实在是救不活了")
    os.chdir("../")
                

for url in urls:
    Soup = parse_index_page(url,3)

    
    
