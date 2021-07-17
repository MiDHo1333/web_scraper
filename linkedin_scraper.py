from bs4 import BeautifulSoup as bs
import re as re
import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
import requests

occurances = {}.fromkeys(['Python','R','Julia','C','C++','Scala','Javascript',
        'SQL','Swift','Bachelors','Masters','Cloud','Tableau'],0)
actual_links_processed = 0




def Scrape_func(links, actual_links_processed, occurences):

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
    cloud_word = 0
    tableau_word = 0

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
                    # if (re.compile('Python').match(word)or re.compile('python').match(word)):
                    #     python_word += 1
                    # elif (re.compile('R').match(word) or re.compile('r').match(word)):
                    #     r_word += 1
                    # elif (re.compile('Julia').match(word) or re.compile('julia').match(word)):
                    #     julia_word += 1
                    # elif (re.compile('\sC\s').match(word) or re.compile('\sc\s').match(word)):
                    #     c_word += 1
                    # elif (re.compile('C\+\+').match(word) or re.compile('c\+\+').match(word)):
                    #     cplus_word += 1
                    # elif (re.compile('C/C\+\+').match(word) or re.compile('c/c\+\+').match(word)):
                    #     c_word += 1
                    #     cplus_word += 1
                    # elif (re.compile('Scala').match(word) or re.compile('scala').match(word)):
                    #     scala_word += 1
                    # elif (re.compile('JavaScript').match(word) or re.compile('Javascript').match(word) or re.compile('javascript').match(word)):
                    #     javascript_word += 1
                    # elif (re.compile('SQL').match(word) or re.compile('sql').match(word)): 
                    #     sql_word += 1
                    # elif (re.compile('Swift').match(word) or re.compile('swift').match(word)): 
                    #     swift_word += 1
                    # elif (re.compile('Bachelors').match(word) or re.compile('bachelors').match(word) or re.compile('B.S.').match(word) or re.compile('BS').match(word) or re.compile('BachelorDegree').match(word)): 
                    #     bach_word += 1
                    # elif (re.compile('Masters').match(word) or re.compile('masters').match(word.lower()) or re.compile('M.S.').match(word) or re.compile('MS').match(word) or re.compile('MasterDegree').match(word)): 
                    #     master_word += 1
                    # elif (re.compile('cloud').match(word.lower())):           
                    #     cloud_word += 1
                    # if (re.compile('tableau').match(word.lower())):           
                    #     tableau_word += 1
                    if word in occurances.keys():
                        occurances[word] += 1
                
                # append words to freq csv


                actual_links_processed += 1
            except:
                print("Mayday")
                pass 

                # occurances.append(python_word)
                # occurances.append(r_word)
                # occurances.append(julia_word)
                # occurances.append(c_word)
                # occurances.append(cplus_word)
                # occurances.append(scala_word)
                # occurances.append(javascript_word)
                # occurances.append(sql_word)
                # occurances.append(swift_word)
                # occurances.append(bach_word)
                # occurances.append(master_word)
                # occurances.append(cloud_word)
                # occurances.append(tableau_word)
job_links = pd.read_excel('job_links.xlsx',header=0,dtype={'Links':str})
Scrape_func(job_links,actual_links_processed,occurances)

print("total companies",actual_links_processed)

#creating frequency.csv and appending the number of occurances for each word
filename = "frequency.csv"
names_of_cols = ['Python','R','Julia','C','C++','Scala','JavaScript','SQL','Swift','Bachelor','Masters','Cloud','Tableau']

with open(filename, 'w') as f:
    f = csv.writer(f)
    # f.writerow(names_of_cols)
    # f.writerow(occurances)
    f.writerow(occurances.keys())
    f.writerow(occurances.values())

fig = plt.figure(figsize = (10, 8))
 
# creating the bar plot
plt.bar(names_of_cols, occurances, color ='blue',
        width = 0.4)
 
plt.xlabel("Specific Requirements")
plt.ylabel("No. of job positions requiring these skills")
plt.title("Frequency of Skills listed in Data Science Positions")
plt.show()

# creating pie chart plot
fig = plt.figure(figsize =(10, 7))
plt.pie(occurances, labels = names_of_cols)
plt.show()