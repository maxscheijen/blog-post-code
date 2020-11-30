import requests
import pandas as pd
import re
import datetime

from datetime import date
from tqdm.notebook import tqdm

from bs4 import BeautifulSoup

import time

filepath = "PATH_TO_CSV"

current_df = pd.read_csv(filepath)
current_df.datetime = pd.to_datetime(current_df.datetime)
last_date = str(current_df.datetime.dt.date.iloc[-1])

today = date.today()
all_dates = pd.date_range(start=last_date, end=today, freq='1D').date.astype(str)
all_dates

def parse_content(url):
  response = requests.get(url)
  content = response.content

  parsed_content = BeautifulSoup(content, "lxml")
  return parsed_content

def extract_data(post_url):
  try:
    post_soup = parse_content(post_url)
    datetime = post_soup.find("span", {"class": "published_WzR_NC-U"}).find("time").text
    title = post_soup.find("h1", {"class": "title_iP7Q1aiP"}).text.strip()
    content = " ".join([post.text for post in post_soup.findAll("p", {"class": "text_3v_J6Y0G"})])
    category = post_soup.find("a", {"class": "link_2imnEnEf"}).text

    data = {
        "raw_date": datetime,
        "title": title,
        "content": content,
        "category": category,
        "url": post_url
    }

    return data
  except:
    "Error: could not extract data from article."

base_article_url = "https://nos.nl"

for date_day in tqdm(all_dates):
  current_df = pd.read_csv(filepath)
  
  base_url_day = "https://nos.nl/nieuws/archief" + "/" + str(date_day)
  soup = parse_content(base_url_day)
  posts = soup.find("div", {"id": "archief"}).findAll("li", {"class": "list-time__item"})
  already = re.findall(date_day, str(posts))
  
  for i, post in enumerate(posts):
    uri = post.find("a")["href"]
    liveblog = re.findall("liveblog", uri)
    url = base_article_url + uri
    if len(liveblog) > 0:
      pass
    else: 
      if current_df['url'].str.contains(url).any():
        pass
      else:
        post_data = extract_data(url)
        new_data = pd.DataFrame(post_data, index=[0])
        new_data['datetime'] = str(date_day) + new_data.raw_date.str.split(",").str.get(1)
        current_df = current_df.append(new_data)
  
  current_df.dropna().to_csv(filepath, index=None)
  pd.read_csv(filepath)

