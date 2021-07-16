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
            #spliting the text in span into individual words
            text_box = (re.split(r'\W+',text_box))
            #number of occurences for these words
            python_word = 0
            r_word = 0
            julia_word = 0
            c_word = 0
            cplus_word = 0
            scala_word = 0
            javascript_word = 0
            sql_word = 0
            swift_word = 0
            bach_word = 0
            master_word = 0

            #for loop to iterate through all words in span to count the importance of them
            for word in text_box:
                if (re.compile('Python') == word or re.compile('python') == word):
                    python_word += 1
                elif (re.compile('R') == word or re.compile('r') == word):
                    r_word += 1
                elif (re.compile('Julia') == word or re.compile('julia') == word):
                    julia_word += 1
                elif (re.compile('C') == word or re.compile('c') == word):
                    c_word += 1
                elif (re.compile('C++') == word or re.compile('c++') == word):
                    cplus_word += 1
                elif (re.compile('C/C++') == word or re.compile('c/c++') == word):
                    c_word += 1
                    cplus_word += 1
                elif (re.compile('Scala') == word or re.compile('scala') == word):
                    scala_word += 1
                elif (re.compile('JavaScript') == word or re.compile('Javascript') == word or re.compile('javascript') == word):
                    javascript_word += 1
                elif (re.compile('SQL') == word or re.compile('sql') == word): 
                    sql_word += 1
                elif (re.compile('Swift') == word or re.compile('swift') == word): 
                    swift_word += 1
                elif (re.compile('Bachelor') == word or re.compile('bachelor') == word or re.compile('B.S.') == word or re.compile('BS') == word or re.compile('BachelorDegree') == word): 
                    bach_word += 1
                elif (re.compile('Master') == word or re.compile('master') == word or re.compile('M.S.') == word or re.compile('MS') == word or re.compile('MasterDegree') == word): 
                    master_word += 1
            
            #appending to new/existing csv file
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
df.to_csv("test2.csv", encoding='utf-8', index=False,header=False,mode='a')