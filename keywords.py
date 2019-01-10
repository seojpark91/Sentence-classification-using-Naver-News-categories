#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import pymongo
from bs4 import BeautifulSoup
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# In[2]:


mysql_client = create_engine("mysql://root:dss@13.209.195.243/world?charset=utf8")
base = declarative_base()
mysql_client


# In[3]:


mongo_client = pymongo.MongoClient('mongodb://13.209.195.243:27017')
mongo_client


# In[4]:


class NaverKeyword(base):
    __tablename__ = "naver"

    id = Column(Integer, primary_key=True)
    rank = Column(Integer, nullable=False)
    keyword = Column(String(50), nullable=False)
    rdate = Column(TIMESTAMP, nullable=False)

    def __init__(self, rank, keyword):
        self.rank = rank
        self.keyword = keyword

    def __repr__(self):
        return "<NaverKeyword {}, {}>".format(self.rank, self.keyword)


# In[5]:


def crawling():
    response = requests.get("https://www.naver.com/")
    dom = BeautifulSoup(response.content, "html.parser")
    keywords = dom.select(".ah_roll_area > .ah_l > .ah_item")
    datas = []
    for keyword in keywords:
        rank = keyword.select_one(".ah_r").text
        keyword = keyword.select_one(".ah_k").text
        datas.append((rank, keyword))
    return datas


# In[6]:


datas = crawling()
datas


# In[7]:


def mysql_save(datas):
    
    keywords = [NaverKeyword(rank, keyword) for rank, keyword in datas]
    
    # make session
    maker = sessionmaker(bind=mysql_client)
    session = maker()

    # save datas
    session.add_all(keywords)
    session.commit()

    # close session
    session.close()


# In[10]:


base.metadata.create_all(mysql_client)


# In[11]:


mysql_save(datas)


# In[12]:


def mongo_save(datas):
    querys = [{"rank":rank, "keyword":keyword} for rank, keyword in datas]
    mongo_client.crawling.naver_keywords.insert(querys)


# In[13]:


mongo_save(datas)


# In[16]:


def send_slack(msg, channel="#dss", username="provision_bot" ):
    webhook_URL = "https://hooks.slack.com/services/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"
    payload = {
        "channel": channel,
        "username": username,
        "icon_emoji": ":provision:",
        "text": msg,
    }
    response = requests.post(
        webhook_URL,
        data = json.dumps(payload),
    )
    return response


# In[17]:


def run():
    # 데이터 베이스에 테이블 생성
    base.metadata.create_all(mysql_client)

    # 네이버 키워드 크롤링
    datas = crawling()

    # 데이터 베이스에 저장
    mysql_save(datas)
    mongo_save(datas)

    # 슬랙으로 메시지 전송
    send_slack("naver crawling done!")


# In[18]:


run()


# In[ ]:




