import psycopg2
import logging
import datetime
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from scraping.utils import *

today = datetime.date.today()
ten_days_ago = datetime.date.today() - datetime.timedelta(10)
from secret import DB_PASSWORD,DB_HOST,DB_NAME,DB_USER, MAILGUN_KEY, API

FROM_EMAIL = 'noreply@find_it.heroky.com'
SUBJECT = 'Список вакансий за {}'.format(today)
template = '''<!doctype html><html lang="en">
                <head><meta charset="utf-8"></head>
                <body>'''
end = '</body></html>'
text = '''Список вакансий, согласно Ваших предпочтений с сервиса JobFinder'''


try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST,
                            password=DB_PASSWORD)
except:
    logging.exception('Unable to open DB -{}'.format(today))
else:
    cur = conn.cursor()
    cur.execute(""" SELECT city_id, speciality_id FROM subscribers_subscribers 
                    WHERE is_active=%s;""", (True,))
    cities_qs = cur.fetchall()
    for pair in cities_qs:
        content = ''
        city = pair[0]
        speciality = pair[1]
        cur.execute(""" SELECT email FROM subscribers_subscribers 
                    WHERE is_active=%s AND city_id=%s AND speciality_id=%s;""", (True, city, speciality))
        email_qs = cur.fetchall()
        emails = [i[0] for i in email_qs]
        cur.execute("""SELECT url,title,description,company FROM scraping_vacancy WHERE city_id=%s AND speciality_id=%s AND timestamp=%s;""", (city,speciality,today))
        jobs_qs = cur.fetchall()
        if jobs_qs:
            for job in jobs_qs:
                content += '<a href="{}" target="_blank">'.format(job[0])
                content += '{}</a><br/>'.format(job[1])
                content += '<p>{}</p>'.format(job[2])
                content += '<p>{}</p><br/>'.format(job[3])
                content += '<hr/><br/><br/>'
                content += '''<h4>Вы получили данное письмо потому, что подписались 
                            на <a href="{}" target="_blank">
                            сервис по рассылке вакансий </a> согласно вашиx 
                            предпочтений<h4><br/>
                            <h5>Спасибо, что Вы с нами! </h5><br/>
                            '''.format('https://jobfinderapp.herokuapp.com/')
            html_m = template + content + end
            for email in emails:
                requests.post(API, auth=("api", MAILGUN_KEY), data={"from":FROM_EMAIL, "to":email,"subject":SUBJECT,"html":html_m})
        else:
            requests.post(API,auth={"api",MAILGUN_KEY},data={"from":FROM_EMAIL,"to":email,
            "subjects":SUBJECT,"text":'Список вакансий по Вашему профилю на сегодня пуст.'})

            # part = MIMEText(html_m, 'html')
            # msg.attach(part)
            # mail.sendmail(FROM_EMAIL, emails, msg.as_string())
            
        # else:
        #     content = '''<h3>На сегодня, список вакансий по 
        #                         Вашему запросу, пуст.</h3> '''
        #     content += '''<h4>Вы получили данное письмо потому, что подписались 
        #                     на <a href="{}" target="_blank">
        #                     сервис по рассылке вакансий </a> согласно вашиx 
        #                     предпочтений<h4><br/>
        #                     <h5>Спасибо, что Вы с нами! </h5><br/>
        #                     '''.format('https://jobfinderapp.herokuapp.com/')
        #     html_m = template + content + end
        #     part = MIMEText(html_m, 'html')
        #     msg.attach(part)
        #     mail.sendmail(FROM_EMAIL, emails, msg.as_string())
            
        # mail.quit()

    conn.commit()
    cur.close()
    conn.close()