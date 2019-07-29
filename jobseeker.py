import requests
import re
import smtplib
from bs4 import BeautifulSoup
import email.message


def sendEmail(content):
    total_message='<h1>Svu Career Path</h1><p>These are new job openings.You can apply through below links</p>'
    for hu in content:
        fd=hu.index('.')
        dup=hu[fd+1:]
        fd2=dup.index('.')
        name=hu[fd+1:fd+fd2+1]
        total_message+='<a href="'+str(hu)+'">'+str(name)+'</a></br>'
    
    to=['mailids']
    for send_mail in to:
        msg = email.message.Message()
        msg['Subject'] = 'Career Path'
        msg['From'] = '**************'
        msg.add_header('Content-Type','text/html')
        s = smtplib.SMTP('smtp.gmail.com',587)
        msg.set_payload(total_message)
        s.starttls()
        s.login('***********','*************')
        msg['To']=send_mail
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()

    
site_links=['https://www.offcampusjobs4u.com/','https://www.enggwave.com/']
dictionary_links={0:[],1:[],2:[]}
print(dictionary_links)
new_links={0:[],1:[],2:[]}
prev_dict_links=[]
url=r'C:\Users\mitta\Desktop\prev_data.txt'
f=open(url,'r')
for h in f:
    prev_dict_links.append(str(h)[:-1])
f.close()
p=0
keywords=['2020','recruitment']
for i in site_links:
    r=requests.get(i)
    soup=BeautifulSoup(r.text,'html.parser')
    for link in soup.find_all('a'):
        p_link=str(link.get('href'))
        for key in keywords:
            if re.findall(key,p_link):
                dictionary_links[p].append(p_link)
                if p_link in prev_dict_links:
                    xiu=0
                else:
                    new_links[p].append(p_link)  
                break
    r.close()
    p+=1

f=open(url,'w')
f.write('l\n')
f.close()
f=open(url,'a')
for k in dictionary_links:
    for inside in dictionary_links[k]:
        f.write(inside+'\n')
f.close()

if new_links:
    new_ids=[]
    for j in new_links:
        if j==0:
            for i in new_links[j]:
                r=requests.get(str(i))
                soup=BeautifulSoup(r.text,'lxml')
                tags=soup.find_all('a')
                for t in tags:
                    if t.text=="Click Here":
                        new_ids.append(t.attrs['href'])
        elif j==1:
            for i in new_links[j]:
                r=requests.get(str(i))
                soup=BeautifulSoup(r.text,'lxml')
                tags=soup.find_all('a')
                for t in tags:
                    if t.text=="Click Here":
                        new_ids.append(t.attrs['href'])
    if len(new_ids)>0:
        sendEmail(new_ids)


