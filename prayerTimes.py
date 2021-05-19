import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import pprint

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

db = df.set_index("Prayer").to_dict()
start = db["Start"]
iqama = db["Iqama"]

corpus = " " + "\n".join("{} {}".format(k, v) for k, v in start.items())

user='noureldin@live.co.uk'
pwd=open("pwd.txt","r").read().strip()
server = smtplib.SMTP('smtp.office365.com', 587)
server.ehlo()
server.starttls()
server.login(user, pwd)
subject = 'Prayer Times'
family = ['abnoureldin@gmail.com',"wnoureldin@gmail.com"]

msg = MIMEText(corpus, 'plain', 'utf-8')
msg['From'] = user
msg['To'] = ', '.join(family)
msg['Subject'] = Header(subject, 'utf-8')

try:
    server.sendmail(user,family, msg.as_string())
    print('email sent')
except:
    print('error')
server.quit()