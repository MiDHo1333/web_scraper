from bs4 import BeautifulSoup as bs
import re as re
import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
import requests


def Scrape_func(links, lowercase_occurences):
    for i in range(len(links)):
        url = links['Links'].values[i].strip(',')
        url += '/detail/recent-activity/shares/'
        res = requests.get(url)
        soup = bs(res.text,'html.parser')
        job_containers = soup.findAll("section",class_="description")
        for container in job_containers:    
            try:
                text_box = container.find("section")
                #spliting the text in span into individual words
                text_box = re.split(r'\W+',str(text_box))
                # for loop to iterate through all words in span to count the importance of them
                for word in text_box:
                    word = word.lower()
                    if word in lowercase_occurances.keys():
                        lowercase_occurances[word] += 1           
            except:
                print("Mayday")
                pass 
            
job_links = pd.read_excel('job_links.xlsx',header=0,dtype={'Links':str})

occurances = {}.fromkeys(['Python','Pandas','Matplotlib','Tensorflow','Numpy','Scikitlearn',
    'AWS','Azure','Kubernetes','R','Tidyverse','Ggplot','Dplyr','Tidyr','Readr','Forcats', 'Spark'
    'SparkR','Julia','C','Scala','Javascript','SQL','Bachelors','Masters','AI','ML','Cloud',
    'Tableau','Tensorflow','Hadoop','PyTorch','Ruby','Github','Django','MongoDB'],0)


lowercase_occurances = {}.fromkeys([k.lower() for k in occurances.keys()],0)
# lowercase_occurances = {}.fromkeys(['python','pandas','matplotlib','tensorflow','numpy',
#     'scikitlearn','aws','azure','kubernetes','r','tidyverse','ggplot','dplyr','tidyr','readr',
#     'forcats','spark','sparkr',julia','c','scala','javascript','sql','bachelors','masters','ai','ml',
#     'cloud','tableau','tensorflow','hadoop','pytorch','ruby','github','django','mongodb'],0)

Scrape_func(job_links,lowercase_occurances)
#creating frequency.csv and appending the number of occurances for each word
filename = "frequency.csv"

with open(filename, 'w') as f:
    f = csv.writer(f)
    f.writerow(occurances.keys())
    f.writerow(occurances.values())

fig = plt.figure(figsize = (10, 8))

# creating the bar plot
plt.bar(occurances.keys(), occurances.values(), color ='blue',
        width = 0.4)
 
plt.xlabel("Specific Requirements")
plt.ylabel("No. of job positions requiring these skills")
plt.title("Frequency of Skills listed in Data Science Positions")
plt.show()

#creating frequency.csv and appending the number of occurances for each word
filename = "frequency_lower.csv"

with open(filename, 'w') as f:
    f = csv.writer(f)
    f.writerow(lowercase_occurances.keys())
    f.writerow(lowercase_occurances.values())

fig = plt.figure(figsize = (10, 8))
 
# creating the bar plot
plt.bar(lowercase_occurances.keys(), lowercase_occurances.values(), color ='blue',
        width = 0.4)
 
plt.xlabel("Specific Requirements")
plt.ylabel("No. of job positions requiring these skills")
plt.title("Frequency of Skills listed in Data Science Positions")
plt.show()

# creating pie chart plot
fig = plt.figure(figsize =(10, 7))
plt.pie(occurances.values(), labels = occurances.keys())
plt.show()