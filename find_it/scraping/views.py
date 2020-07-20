from django.shortcuts import render
from django.db import IntegrityError
from django.http import Http404
from .utils import *
from .models import *
import datetime
from .forms import FindVacancyForm

def index(request):
    form = FindVacancyForm
    return render(request,'scraping/home.html', {'form':form})

def vacancy_list(request):
    today = datetime.date.today()
    form = FindVacancyForm
    if request.GET:
        try:
            city_id = int(request.GET.get('city'))
            speciality_id = int(request.GET.get('speciality'))
        except ValueError:
            raise Http404('Страница не найдена')
        context = {}
        context['form'] = form
        qs = Vacancy.objects.filter(city=city_id, speciality=speciality_id) #, timestamp=today)
        if qs:
            context['jobs'] = qs
            return render(request,'scraping/list.html',context)
    return render(request,'scraping/list.html', {'form':form})

def scrap(request):
    city = City.objects.get(name='Минск')
    speciality = Speciality.objects.get(name='Python')
    url_qs = Url.objects.filter(city=city,speciality=speciality)
    site = Site.objects.all()
    url_tut = url_qs.get(site=site.get(name='jobs.tut.by')).url_adress
    url_bel = url_qs.get(site=site.get(name='belmeta.com')).url_adress
    jobs = []
    jobs.extend(tut_pars(url_tut))
    jobs.extend(bel_pars(url_bel))
    # v = Vacancy.objects.filter(city=city.id, speciality=speciality.id).values('url')
    # url_list = [i['url']for i in v] #generators list of urls
    for job in jobs:
        # if job['href'] not in url_list: #check in db
        vacancy = Vacancy(city=city, speciality=speciality, url=job['href'],
                        title=job['title'], description=job['description'], company=job['company'])
        try:
            vacancy.save()                
        except IntegrityError:
            pass
    return render(request,'scraping/list.html',{'jobs':jobs})
