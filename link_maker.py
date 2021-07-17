'''linked_maker.py
gets list of ids from initial url
To Do: Create valid links to sift through job requirements. 
Example: https://www.linkedin.com/jobs/view/data-scientist-at-cvs-health-2652878200?refId=YDF7%2BPAzajYP39710xFV3Q%3D%3D&trackingId=H%2FkZRfHnlk%2BXQsFxJAQJxw%3D%3D&position=17&pageNum=0&trk=public_jobs_jserp-result_search-card
'''
from bs4 import BeautifulSoup as bs
import re as re
import pandas as pd
import os
import requests

for i in range(20):
    url = f"https://www.linkedin.com/jobs/search/?currentJobId=2557487241&keywords=data%20scientist&position=1&pageNum={i}"
    # url = "https://www.linkedin.com/jobs/search/?currentJobId=2557487241&keywords=data%20scientist"
    res = requests.get(url)
    soup = bs(res.text,'html.parser')
    job_container = soup.findAll("a",class_="base-card__full-link")
    id_list = []
    for job in job_container:
        job = re.findall(r'\d+',str(job))
        id_list.append(job[0])

print(len(id_list))
df = pd.DataFrame(id_list)
df.to_csv("job_id.csv", encoding='utf-8', index=False,header=False,mode='a')
