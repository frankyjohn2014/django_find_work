import requests
from bs4 import BeautifulSoup as BS
import codecs
import time

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
           'Accept':'text/html, application/xhtml+xml, application/xml;q=0.9,*/*;q=0.8'
}

start_url = 'https://jobs.tut.by/search/vacancy?area=1002&st=searchVacancy&fromSearch=true&text=python'
req = session.get(start_url, headers=headers)
bsObj = BS(req.content, "html.parser")
jobs = []
url = []
base_url = 'https://jobs.tut.by'
url.append(start_url)
pagination = bsObj.find_all('a',attrs={'data-qa':'pager-page'})
for link in pagination:
    link_pag = link.get('href')
    url.append(base_url + link_pag)
time.sleep(2)
for now_url in url:
    print(now_url)
    req = session.get(now_url, headers=headers)
    time.sleep(2)
    bsObj = BS(req.content, "html.parser")
    all_div = bsObj.find_all('div',attrs={"class":"vacancy-serp-item"})
    for div in all_div:
        title = div.find('a', attrs={"data-qa":"vacancy-serp__vacancy-title"}) # title #href
        # print(title.text)
        employer = div.find('a', attrs={"data-qa":"vacancy-serp__vacancy-employer"})
        # print(employer.text)
        descrp = div.find('div', attrs={"data-qa":"vacancy-serp__vacancy_snippet_responsibility"})
        # print(descrp.text)
        href = div.find('a', attrs={"data-qa":"vacancy-serp__vacancy-title"})
        # print(href.get('href'))
        logo = div.find('img', attrs={"class":"vacancy-serp-item__logo"})
        # if logo:
        #     print(logo.get('src'))
        # else:
        #     print('-')
        date = div.find('span', attrs={"class":"vacancy-serp-item__publication-date"}) # title #href
        # print(date.text)
        jobs.append({'href':href.get('href'),
                     'title': title.text,
                     'descript':descrp.text,
                     'company':employer.text})

# # data = bsObj.prettify()#.encode('utf8')
handle = codecs.open('div.html','w', 'utf-8')
handle.write(str(jobs))
handle.close  