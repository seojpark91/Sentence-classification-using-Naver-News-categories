# Sentence Classification using Naver News categories (Politics, Economics, Society, Life/Culture, World, IT/Science)
# 네이버 뉴스 카테고리를 통한 input 문장 분류 (정치, 경제, 사회, 생활/문화, 세계, IT/과학)

## Motivation :
- implement a sentence classifier with multinomial naive bayes model 
- The model was trained with `article_2016-06-01.pkl` which is the file of Naver news titles 

## Requirements:
```
requests
bs4
numpy
pandas
mysqlclient
sqlalchemy
pymongo==2.8.1
scikit-learn==0.19.1
scipy
flask
```

## Contents:
- make_model.ipynb - make a sentence classifier with multinomial naive bayes model and finding a smoothing parameter   
- find_variable.py - full code described in make_model.ipynb  
- article.py - basic web application made with Flask  
- templates/index.html - includes html file  

## Side assignments:
- `keyword_class.ipynb` and `keywords.ipynb`shows step by step guide to save real time top Naver top 20 keywords and store them to MongoDB and mySQL using `pymongo`and `sqlalchemy`
