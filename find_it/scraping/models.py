from django.db import models

class City(models.Model):
    name = models.CharField(max_length=50,verbose_name='Город')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Город'


class Speciality(models.Model):
    name = models.CharField(max_length=50,verbose_name='Специальность')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

class Site(models.Model):
    name = models.CharField(max_length=50,verbose_name='Сайт для поиска')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сайт для поиска'
        verbose_name_plural = 'Сайты для поиска'

class Url(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE,verbose_name='Город')
    speciality = models.ForeignKey(Speciality,max_length=250,verbose_name='Специальность',on_delete=models.CASCADE)
    site = models.ForeignKey(Site,verbose_name='Сайт для поиска',on_delete=models.CASCADE)
    url_adress = models.CharField(max_length=250, unique=True, verbose_name='Адрес для поиска')

    def __str__(self):
        return 'Специальность {} в г.{} на сайте {}'.format(self.speciality,self.city,self.site)

    class Meta:
        verbose_name = 'Адрес для поиска'
        verbose_name_plural = 'Адреса для поиска'

class Vacancy(models.Model):
    url = models.CharField(max_length=250, unique=True, verbose_name='Адрес вакансии')
    title = models.CharField(max_length=250,verbose_name='Заголовок вакансии')
    description = models.TextField(blank=True,verbose_name='Описание вакансии')
    company = models.CharField(max_length=250,blank=True,null=True,verbose_name='Название компании')
    city = models.ForeignKey(City, on_delete=models.CASCADE,verbose_name='Город')
    speciality = models.ForeignKey(Speciality,max_length=250,verbose_name='Специальность',on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True)
  
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансию'
        verbose_name_plural = 'Вакансии'