import pandas as pd 
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def getMovieLink(links):
    movie_link = [] 
    unique_list =[]
 

    for link_tag in links: 
        link_url = link_tag.get('href',"No Url Found") 
        
        #omit vote and search urls

        if  "/vote"  not in link_url: 
            if "/search" not in link_url:
                base_url = "https://www.imdb.com"
                complete_url = urljoin(base_url, link_url)
                complete_url += "?ref_=adv_li_tt"
                movie_link.append(complete_url)
    
    #remove duplicates
    
    for item in movie_link:
        if item not in unique_list:
            unique_list.append(item)
    
    return unique_list

def getMovieImages(images):
    movie_image=[]
    for image_tag in images:
        img_url = image_tag.get('src',"No Image Found")
        movie_image.append(img_url)
    return movie_image
 

def getMovieTitles(links,pageFirstTitle):
    movie_titles=[]
    start_appending = False 


    for link in links:
        title = link.text.strip()

        if title != "Next »" and title != "X" and title != "":
            if title == pageFirstTitle.strip():
               start_appending = True 
            
            if start_appending:
               movie_titles.append(title)

    return movie_titles

def getMovieRatings(ratings):
    movie_ratings =[]
    for rating in ratings:
        rating_text = rating.text
        isNum = rating_text.replace('.', '', 1).isdigit()  # Check if the string contains only numeric characters (including decimal point)
        if isNum is True:
           movie_ratings.append(rating_text)
    return movie_ratings

def getMovieYear(years):
    movie_year = [] 
    for year in years:
        movie_year.append(year.text)
    return movie_year


url = "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating" 

req = requests.get(url).content 

soup = BeautifulSoup(req,'html.parser')

#use lamba function to get tags related to title

links = soup.find_all('a',href=lambda href: href and "/title/" in href)
images = soup.find_all('img')
ratings = soup.find_all('strong') 
years = soup.find_all('span',class_="lister-item-year")


movie_links = getMovieLink(links)
movie_titles = getMovieTitles(links,"The Shawshank Redemption")
movie_ratings = getMovieRatings(ratings)
movie_years = getMovieYear(years)


data = {"links":movie_links,"titles":movie_titles,"ratings":movie_ratings,"years":movie_years}
df = pd.DataFrame(data=data)

d = json.dumps(data)
l = json.loads(d)

with open("movies.json","w") as f:
    f.write(d)
    f.close()








