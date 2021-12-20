from django.contrib import auth
from django.db import models
from django.template.backends import django
import django.utils.timezone
from django.utils import translation
from django.core import validators
from django.contrib.auth.models import User
# Create your models here.

class Pd(models.Model):
    nom = models.IntegerField(unique = True, verbose_name="Номер дела")
    snils = models.CharField(max_length=14, verbose_name="СНИЛС", 
                            validators = [validators.RegexValidator(regex="^\d{3}-\d{3}-\d{3} \d{2}$")], 
                            error_messages={'invalid': 'Формат СНИЛС д.б. 123-456-789 10'})
    fam = models.CharField(max_length=25, verbose_name="Фамилия")
    name = models.CharField(max_length=25, verbose_name="Имя")
    fname = models.CharField(max_length=25, null =True, blank=True, verbose_name="Отчество")
    dr = models.DateField(verbose_name="Дата рождения")
    zind = models.CharField(max_length=6, verbose_name="Индекс")
    gor = models.ForeignKey('VocNsp', null=True, on_delete=models.PROTECT, verbose_name="Населенный пункт")
    ul = models.ForeignKey('VocUlc', null=True, on_delete=models.PROTECT, verbose_name="Улица")
    dom = models.CharField(max_length=8, verbose_name="Дом")
    kor = models.CharField(max_length=2, null =True, blank=True, verbose_name="Корпус")
    kvar = models.CharField(max_length=4, null =True, blank=True, verbose_name="Квартира")
    dnp = models.DateField(verbose_name="Дата назначения пенсии")
    dlp = models.DateField(verbose_name="Дата прекращения выплаты")
    dhp = models.DateField(verbose_name="Дата хранения ПО")
    drr = models.DateField(null =True, blank=True, verbose_name="Дата ревизии")
    post = models.TextField(null=True, blank=True, verbose_name="Комментарии")
    link = models.CharField(null=True, blank=True, max_length=80, verbose_name="Категории умершего")
    link1 = models.ForeignKey('CatPens', related_name='catp1', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Категория1 умершего")
    link2 = models.ForeignKey('CatPens', related_name='catp2', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Категория2 умершего")
    link3 = models.ForeignKey('CatPens', related_name='catp3', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Категория3 умершего")
    ds = models.DateField(null =True, blank=True, verbose_name="Дата смерти")
    sud = models.CharField(null=True, blank=True, max_length=4, verbose_name="Серия удостоверения")
    nud = models.IntegerField(null=True, blank=True, verbose_name="Номер удостоверения")
    nvidp = models.ForeignKey('VidPens', null=True, on_delete=models.PROTECT, verbose_name="Вид пенсии")
    date_create = models.DateField(auto_now_add=True,)
    #user_create = models.ForeignKey('auth.user', on_delete=models.PROTECT, related_name='user_create')
    date_update = models.DateField(auto_now=True,)
    #user_update = models.ForeignKey('auth.user', null=True, on_delete=models.PROTECT, verbose_name="пользователь отредактировал", related_name='user_update',default=get_current_user)

    def save(self, *args, **kwargs):
        self.fam = self.fam.upper()
        self.name = self.name.upper()
        if self.fname:
            self.fname = self.fname.upper()
        #self.user_create = auth.username
        #self.user_update=auth.username
        #self.gor = self.gor.upper()
        #self.ul = self.ul.upper()
        super(Pd,self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Архивные дела'
        verbose_name = 'Архивное дело'
        ordering = ['fam', 'name', 'fname']
        indexes = [
            models.Index(fields=['nom'], name='ord_by_nom'),
            models.Index(fields=['fam', 'name', 'fname'], name='ord_by_fio')
        ]

class VidPens(models.Model):
    nvidp = models.CharField(max_length=35, verbose_name="Вид пенсии")
    def __str__(self):
        return self.nvidp

    class Meta:
        verbose_name_plural = 'Виды пенсий'
        verbose_name = 'Вид пенсии'
        ordering = ['id']
    

class CatPens(models.Model):
    ncatp = models.CharField(max_length=45, verbose_name="Категория получателя")
    def __str__(self):
        return self.ncatp

    class Meta:
        verbose_name_plural = 'Категории получателя'
        verbose_name = 'Категория получателя'
        ordering = ['id']

class VocNsp(models.Model):
    name = models.CharField(max_length=45, verbose_name="Населенный пункт")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Населенные пункты'
        verbose_name = 'Населенный пункт'
        ordering = ['id']


class VocUlc(models.Model):
    kodnsp =models.ForeignKey('VocNsp', null=True, on_delete=models.PROTECT, verbose_name="Город")
    name = models.CharField(max_length=45, verbose_name="Улица")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Улицы'
        verbose_name = 'Улица'
        ordering = ['kodnsp', 'name']

class VocDistrict (models.Model):
    koddistrict = models.CharField(max_length=4, verbose_name='Код Района')
    namedistrict = models.CharField(max_length=55, verbose_name='Наименование Района')
    def __str__(self):
        return self.namedistrict

    class Meta:
        verbose_name_plural = 'Коды Районов'
        verbose_name = 'Код Района'
        ordering = ['id']