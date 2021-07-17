from bs4 import BeautifulSoup as bs
import re as re
import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
import requests

occurances = []

def Scrape_func(links):
    url = "https://www.linkedin.com/jobs/view/2644245283/?alternateChannel=search&refId=V7qh%2F7YOXM6rnRdfIu8lCA%3D%3D&trackingId=YCM8qAXxtQH80KA9b2C6hA%3D%3D"
    url += 'detail/recent-activity/shares/'
    res = requests.get(url)
    soup = bs(res.text,'html.parser')
    job_containers = soup.findAll("section",class_="description")
    for container in job_containers:    
        try:
            text_box = container.find("section")
            # #spliting the text in span into individual words
            text_box = re.split(r'\W+',str(text_box))
            print(text_box)
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
                elif (re.compile('C\+\+') == word or re.compile('c\+\+') == word):
                    cplus_word += 1
                elif (re.compile('C/C\+\+') == word or re.compile('c/c\+\+') == word):
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
                elif (re.compile('Bachelors') == word or re.compile('bachelors') == word or re.compile('B.S.') == word or re.compile('BS') == word or re.compile('BachelorDegree') == word): 
                    bach_word += 1
                elif (re.compile('masters').match(word.lower()) or re.compile('M.S.').match(word) or re.compile('MS').match(word) or re.compile('MasterDegree').match(word)): 
                    master_word += 1
                elif (re.compile('cloud').match(word.lower())):           
                    cloud_word += 1
                elif (re.compile('tableau').match(word.lower())):           
                    tableau_word += 1
            
            #append words to freq csv
            occurances.append(python_word)
            occurances.append(r_word)
            occurances.append(julia_word)
            occurances.append(c_word)
            occurances.append(cplus_word)
            occurances.append(scala_word)
            occurances.append(javascript_word)
            occurances.append(sql_word)
            occurances.append(swift_word)
            occurances.append(bach_word)
            occurances.append(master_word)
            occurances.append(cloud_word)
            occurances.append(tableau_word)
        except:
            print("Mayday")
            pass 


job_links = pd.read_excel('job_links.xlsx',index_col=None,header=None,nrows=1)
for j in range(len(job_links)):
    Scrape_func(job_links[j])

#creating frequency.csv and appending the number of occurances for each word
filename = "frequency.csv"
names_of_cols = ['Python','R','Julia','C','C++','Scala','JavaScript','SQL','Swift','Bachelor','Masters','Cloud','Tableau']
with open(filename, 'w') as f:
    f = csv.writer(f)
    f.writerow(names_of_cols)
    f.writerow(occurances)

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