#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import json
import pymongo
from bs4 import BeautifulSoup
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# In[4]:


base = declarative_base()
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


# In[7]:


class NaverKeywords:
    #
    
    def __init__(self, ip, base):
        self.mysql_client = create_engine("mysql://root:dss@{}/world?charset=utf8".format(ip))
        self.mongo_client = pymongo.MongoClient('mongodb://{}:27017'.format(ip))
        self.datas = None
        self.base = base
        
    def crawling(self):
        response = requests.get("https://www.naver.com/")
        dom = BeautifulSoup(response.content, "html.parser")
        keywords = dom.select(".ah_roll_area > .ah_l > .ah_item")
        datas = []
        for keyword in keywords:
            rank = keyword.select_one(".ah_r").text
            keyword = keyword.select_one(".ah_k").text
            datas.append((rank, keyword))
        self.datas = datas
    
    
    def mysql_save(self):
        
        # make table
        self.base.metadata.create_all(self.mysql_client)
        
        # parsing keywords
        keywords = [NaverKeyword(rank, keyword) for rank, keyword in self.datas]

        # make session
        maker = sessionmaker(bind=self.mysql_client)
        session = maker()

        # save datas
        session.add_all(keywords)
        session.commit()

        # close session
        session.close()
        
    def mongo_save(self):
        
        # parsing querys
        keyowrds = [{"rank":rank, "keyword":keyword} for rank, keyword in self.datas]
        
        # insert keyowrds
        self.mongo_client.crawling.naver_keywords.insert(keyowrds)
        
    def send_slack(self, msg, channel="#dss", username="provision_bot" ):
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
    
    def run(self):
        self.crawling()
        self.mysql_save()
        self.mongo_save()
        self.send_slack("naver crawling done!")
        print("execute done!")


# In[8]:


nk = NaverKeywords("13.209.195.243", base)
nk.run()
print("민재가도와줌!")


# In[ ]:




