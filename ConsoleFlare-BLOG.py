import requests
from bs4 import BeautifulSoup
import lxml
import openpyxl
import pandas as pd

# Scraping the data from all the web-pages...
Len,blog_list=int(input("Total No of Web Pages :")),[]
for page_name in range(0,Len):
    url=f'https://consoleflare.com/blog/category/data-science/page/{page_name+1}/'
    console_flare=requests.get(url)
    # print(console_flare)

    console_flare_txt=console_flare.content
    # print(console_flare_txt)

    console_flare_soup=BeautifulSoup(console_flare_txt,'lxml')
    # print(console_flare_soup)

    # console_flare_title=console_flare_soup.find('title')
    # print(console_flare_title)
    console_flare_data=console_flare_soup.find_all('div','thumb-cat-wrap')
    # print(console_flare_data)
    new_trend_list=[]
    for trends in console_flare_data:
        trending=trends.find('div','post-cats-list').get_text()
        new_trend_list.append(trending.replace(' ','-').replace('\n',' ').lstrip(' ').rstrip(' '))
    # print(new_trend_list)
    trend_list=[]
    for st_1 in new_trend_list:
        trend_dict={}
        new_list=st_1.split(' ')
        trend_dict['Trending']=new_list
        trend_list.append(trend_dict)
    # print(trend_list)
    console_flare_data_1=console_flare_soup.find_all('div','entry-cat')
    # print(console_flare_data_1)
    publish_time=[]
    for publish in console_flare_data_1:
        time_publish=publish.find('span','posted-on').get_text()
        publish_time.append(time_publish.replace(',',''))
    # print(publish_time)
    new_publish_list=[]
    for new_publish in publish_time:
        if len(new_publish)<=16:
            new_publish_list.append(new_publish)
        else:
            index_1=new_publish.find('02')
            # print(index_1)
            new_publish_list.append(new_publish[0:index_1+3])
            new_publish_list.append(new_publish[index_1+3:])
    # print(new_publish_list)
    publish_list=[]
    for st_2 in new_publish_list:
        publish_dict=dict()
        publish_dict['Published_Time']=st_2
        publish_list.append(publish_dict)
    # print(publish_list)
    console_topic=console_flare_soup.find_all('header','entry-header')
    blog_topic=list()
    for topic in console_topic:
        topic_dict=dict()
        console_flare_topic=topic.find('h2','entry-title').get_text()
        topic_dict["Blog Topic"]=console_flare_topic
        blog_topic.append(topic_dict)
    # print(blog_topic)
    #print("......................................................")
    for trends,publish,topic in zip(trend_list,publish_list,blog_topic):
        blog_dict=dict()
        blog_dict['Trending']=trends['Trending']
        blog_dict['Published_Time']=publish['Published_Time']
        blog_dict['Blog Topic']=topic['Blog Topic']
        blog_list.append(blog_dict)
print(f"Blog Contents : {blog_list}")
print("......................................................")

# Transformation of Json Data into a Relational Table/Matrix
Blog_Content=pd.json_normalize(blog_list)
print(Blog_Content)

# Transformation of Matrix into an Excel
Blog_Content.to_excel('Console_Flare_Blog.xlsx',index=False)








