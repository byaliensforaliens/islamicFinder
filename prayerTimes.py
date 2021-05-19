import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

url = "http://www.salahadeenmosque.org.uk/"

r = requests.get(url)
html_doc = r.text
soup = BeautifulSoup(html_doc, 'html.parser')

prayer_names = soup.find_all("th",{"class":"prayerName"})
p_n = []
for i in prayer_names:
    p_n.append(i.text)
p_n.remove("Sunrise")

prayer_start = soup.find_all("td",{"class":"begins"})
p_s = []
for j in prayer_start:
    p_s.append(j.text)

iqama_time = soup.find_all("td",{"class":"jamah"})
i_s = []
for k in iqama_time:
    i_s.append(k.text)

df = pd.DataFrame({"Prayer":p_n,
                    "Start":p_s,
                    "Iqama":i_s})

print(df)