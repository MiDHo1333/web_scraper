'''linked_maker.py
gets list of ids from initial url
To Do: Create valid links to sift through job requirements.
Example: 
From : 2652878200 
To: https://www.linkedin.com/jobs/view/2636853058/?alternateChannel=search&refId=V7qh%2F7YOXM6rnRdfIu8lCA%3D%3D&trackingId=YCM8qAXxtQH80KA9b2C6hA%3D%3D

'''
from bs4 import BeautifulSoup as bs
import re as re
import pandas as pd
import os
import requests

max_positions = 23 #positions per page, limited by LinkedIn
max_pages = 10
id_list = []

for i in range(max_positions):
    for j in range(max_pages): 
        url = f"https://www.linkedin.com/jobs/search/?currentJobId=2557487241&keywords=data%20scientist&position={i}&pageNum={j}"
        res = requests.get(url)
        soup = bs(res.text,'html.parser')
        job_container = soup.findAll("a",class_="base-card__full-link")
        
        for job in job_container:
            job = re.findall(r'\d+',str(job))

            id_list.append(job[0]+",")


print(len(id_list))
df = pd.DataFrame(id_list)
df.to_csv("job_id.csv", encoding='utf-8', index=False,header=False,mode='a')
