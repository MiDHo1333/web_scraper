from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re as re
import time
import pandas as pd
import os

#init selenium
# PATH = input("Enter the Webdriver path: ")
USERNAME = os.environ['LINKEDIN_USERNAME']
PASSWORD = os.environ['LINKEDIN_PASSWORD']

#init web driver
# driver = webdriver.Chrome(PATH)
driver = webdriver.Chrome()

#init linkedin
driver.get("https://www.linkedin.com/uas/login")
time.sleep(1)
email=driver.find_element_by_id("username")
email.send_keys(USERNAME)
password=driver.find_element_by_id("password")
password.send_keys(PASSWORD)
time.sleep(1)
password.send_keys(Keys.RETURN)

#lists of profiles, posts, and authors
post_links,post_texts,post_names = [],[],[]


def Scrape_func(a,b,c):
    name = a[28:-1]
    page = a
    time.sleep(10)

    #slice profile name
    driver.get(page + 'detail/recent-activity/shares/')  
    company_page = driver.page_source   

    linkedin_soup = bs(company_page.encode("utf-8"), "html")
    linkedin_soup.prettify()
    containers = linkedin_soup.findAll("article",{"class":"jobs-description__container jobs-description__container--condensed"})
    print("Fetching data from account: "+ name)
    iterations = 0
    # nos = int(input("Enter number of posts: "))
    for container in containers:

        try:
            text_box = container.find("div",{"class":"jobs-description__content jobs-description-content jobs-description__content--condensed"})
            text_box = container.find("span")
            
            b.append(text_box)
            c.append(name)

        except:
            print("Mayday")
            pass 

n = int(input("Enter the number of entries: "))
for i in range(n):
    post_links.append(input("Enter the link: "))
for j in range(n):
    Scrape_func(post_links[j],post_texts,post_names)

        
driver.quit()

# Saving the data
data = {
    "Name": post_names,
    "Content": post_texts,
}

df = pd.DataFrame(data)
print(df)
df.to_csv("test2.csv", encoding='utf-8', index=False,mode='a')