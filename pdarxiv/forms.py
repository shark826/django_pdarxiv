# from typing_extensions import Required
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models import Max
from django.forms import ModelForm, fields, models, widgets, DateField
from django.db.models.fields import DateField, DecimalField
from django.forms.widgets import DateInput, SelectDateWidget
from .models import Pd, VidPens, CatPens, VocNsp, VocUlc
from ajax_select.fields import AutoCompleteSelectMultipleField
import datetime


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class PdFormC(ModelForm):
    dr = forms.DateField(label='Дата рождения', widget=forms.TextInput(attrs={'type': 'date'}))
    ds = forms.DateField(label='Дата смерти', widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    dnp = forms.DateField(label='Дата назначения пенсии', widget=forms.TextInput(attrs={'type': 'date'}))
    dlp: DateField = forms.DateField(label='Дата прекращения выплаты', widget=forms.TextInput(attrs={'type': 'date'}))
    dhp = forms.DateField(label='Дата хранения ПО', widget=forms.TextInput(attrs={'type': 'date'}))
    drr = forms.DateField(label='Дата ревизии', widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    nom = forms.DecimalField(label='Номер дела', max_digits=8, decimal_places=0, min_value=1)
    snils = forms.CharField(label='СНИЛС', widget=forms.TextInput(attrs={'data-mask': "000-000-000 00"}))

    # post = forms.Textarea(attrs={'rows':'3', 'cols':'120'})

    class Meta:
        model = Pd
        fields = ('nom', 'snils', 'fam', 'name', 'fname', 'dr', 'ds',
                  'zind', 'gor', 'ul', 'dom', 'kor', 'kvar',
                  'nvidp', 'dnp', 'dlp', 'dhp', 'drr',
                  'post', 'link', 'link1', 'link2', 'link3', 'sud', 'nud', )
        labels = {'snils': 'Ну введи СНИЛС !!!', 'fam': 'А тут Фамилия'}
        # field_classes = {'nom': DecimalField}
        # widgets = {'snils': forms.TextInput(attrs={'data-mask':"000-000-000 00", 'size':"28"})}
        # widgets = {'post': forms.Textarea(attrs={'rows':'3', 'cols':'120'})}
        widgets = {'sud': forms.TextInput(attrs={'size': 3}), 'nud': forms.TextInput(attrs={'size': 5}),
                   'dom': forms.TextInput(attrs={'size': 4}),
                   'kor': forms.TextInput(attrs={'size': 3}),
                   'kvar': forms.TextInput(attrs={'size': 4}),
                   'post': forms.Textarea(attrs={'rows': '3', 'cols': '84'}),
                   'snils': forms.TextInput(
                       attrs={'placeholder': '123-456-789 10', 'pattern': "^\d{3}-\d{3}-\d{3} \d{2}$", 'size': 16}),
                   'nom': forms.NumberInput(attrs={'size': 8}),
                   }
        error_messages = {
            'nom': {'unique': 'Формат СНИЛС д.б. 123-456-789 10'}
        }

    def __init__(self, *args, **kwargs):
        super(PdFormC, self).__init__(*args, **kwargs)
        newnom = self.newnom()
        self.fields['nom'].error_messages = {
            'unique': ("Номер дела уже используется"),
            'max_digits': ("в номере не должно быть более 8 цифр"),
            'min_value': ("номер не может быть меньше 1")
        }
        self.fields['snils'].error_messages = {
            'invalid': ("СНИЛС не того формата")
        }
        self.initial['nom'] = newnom

    def newnom(self):
        nnom = self.fields['nom']
        # print (nnom)
        nnn = Pd.objects.values('nom').annotate(max_nom=Max('nom')).order_by('nom').last()
        nnn2 = nnn['max_nom'] + 1
        # print( Pd.objects.values('nom').annotate(max_nom = Max('nom')).order_by() )
        # print()
        # print( nnn2 )
        # print(nnom)
        return nnn2

    # проверка полей на корректность ввода по правилам ПФР
    def clean(self):
        cleaned_data = super().clean()
        dhp: datetime = self.cleaned_data['dhp']
        dnp: datetime = self.cleaned_data['dnp']
        dr: datetime = self.cleaned_data['dr']
        ds: datetime = self.cleaned_data['ds']
        dlp: datetime = self.cleaned_data['dlp']
        nvidp = self.cleaned_data['nvidp']
        zind = self.cleaned_data['zind']

        # nvidp = nvidp.strim()

        if not zind.isdigit():
            raise ValidationError(f"Почтовый индекс должен содержать только цифры, а не Ваше {zind}")

        if nvidp == 'vp':
            print('nmhgmgtratatata')

        if dhp.year - dlp.year > 20:
            raise ValidationError('Дата хранения больше 20 лет')

        if dr > datetime.date.today():
            raise ValidationError('Дата рождения в будующем!!!')

        if ds:
            if ds < dnp:
                raise ValidationError('Дата смерти меньше назначения????')
        if dlp < dnp:
            raise ValidationError('Дата прекращеня должна быть больше даты назначения')
        if dlp.day > 1:
            print(self.cleaned_data['nvidp'])
            raise ValidationError('Дата прекращеня должна быть первого числа')
            # raise ValidationError('Дата прекращеня должна приходиться на начало месяца')

        return

    def clean_snils(self):
        snils = self.cleaned_data['snils']
        ks_pd = snils[12:14]
        '''Проверка контрольного числа проводится только для номеров 
            больше номера 001-001-998.
            (вот это что-то новое – будет уточнено в ОПФР)

            Контрольное число СНИЛС рассчитывается следующим образом:
            * Каждая цифра СНИЛС умножается на номер своей позиции 
              (позиции отсчитываются с конца);
            * Полученные произведения суммируются;
            * Если сумма меньше 100, то контрольное число равно самой сумме;
            * Если сумма равна 100 или 101, то контрольное число равно 00;
            * Если сумма больше 101, то сумма делится нацело на 101 и контрольное число определяется
              остатком от деления аналогично предыдущим двум пунктам.'''
        ks_pfr = 0
        ks_pfr = ks_pfr + 9 * int(snils[0:1])
        ks_pfr = ks_pfr + 8 * int(snils[1:2])
        ks_pfr = ks_pfr + 7 * int(snils[2:3])
        ks_pfr = ks_pfr + 6 * int(snils[4:5])
        ks_pfr = ks_pfr + 5 * int(snils[5:6])
        ks_pfr = ks_pfr + 4 * int(snils[6:7])
        ks_pfr = ks_pfr + 3 * int(snils[8:9])
        ks_pfr = ks_pfr + 2 * int(snils[9:10])
        ks_pfr = ks_pfr + 1 * int(snils[10:11])

        if ks_pfr == 100 or ks_pfr == 101:
            ks_pfr == 0
        elif ks_pfr > 101:
            ks_pfr = ks_pfr % 101

        ks_pfr = str(ks_pfr).rjust(2, '0')

        if ks_pfr != ks_pd:
            raise ValidationError(f"Контрольное число в СНИЛС д.б. {ks_pfr}, а вы написали {ks_pd}")
        return snils

    '''
    def clean_dlp(self):
        dlp: datetime = self.cleaned_data['dlp']
        if dlp.day > 1:
            raise ValidationError('Ебанись Дата прекращеня должна быть первого числа')
            #raise ValidationError('Дата прекращеня должна приходиться на начало месяца')
            dlp = self.cleaned_data['dlp']
        return dlp
    
    def clean_dhp(self):
        dhp: datetime = self.cleaned_data['dhp']
        ds: datetime = self.cleaned_data['ds']
        dlp: datetime = self.cleaned_data['dlp']
        if dhp.year - dlp.year > 20:
            raise ValidationError('Дата хранения что-то охуенно большая')
            #raise ValidationError('Дата хранения больше 20 лет')

        return dhp

    '''



class PdForm(ModelForm):
    # gor = AutoCompleteSelectMultipleField('gor')
    dr = forms.DateField(label='Дата рождения', widget=forms.TextInput(attrs={'type': 'date'}))
    ds = forms.DateField(label='Дата смерти', widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    dnp = forms.DateField(label='Дата назначения пенсии', widget=forms.TextInput(attrs={'type': 'date'}))
    dlp: DateField = forms.DateField(label='Дата прекращения выплаты', widget=forms.TextInput(attrs={'type': 'date'}))
    dhp = forms.DateField(label='Дата хранения ПО', widget=forms.TextInput(attrs={'type': 'date'}))
    drr = forms.DateField(label='Дата ревизии', widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    nom = forms.DecimalField(label='Номер дела', max_digits=8, decimal_places=0, min_value=1)
    snils = forms.CharField(label='СНИЛС', widget=forms.TextInput(attrs={'data-mask': "000-000-000 00"}))

    class Meta:
        model = Pd
        fields = ('nom', 'snils', 'fam', 'name', 'fname', 'dr', 'ds',
                  'zind', 'gor', 'ul', 'dom', 'kor', 'kvar',
                  'nvidp', 'dnp', 'dlp', 'dhp', 'drr', 'post',
                  'link', 'link1', 'link2', 'link3', 'sud', 'nud', )
        labels = {'snils': 'Ну введи СНИЛС !!!', 'fam': 'А тут Фамилия'}
        # field_classes = {'nom': DecimalField}
        # widgets = {'snils': forms.TextInput(attrs={'data-mask':"000-000-000 00", 'size':"28"})}
        # widgets = {'post': forms.Textarea(attrs={'rows':'3', 'cols':'120'})}
        widgets = {'sud': forms.TextInput(attrs={'size': 3}), 'nud': forms.TextInput(attrs={'size': 5}),
                   'dom': forms.TextInput(attrs={'size': 4}),
                   'kor': forms.TextInput(attrs={'size': 3}),
                   'kvar': forms.TextInput(attrs={'size': 4}),
                   'post': forms.Textarea(attrs={'rows': '3', 'cols': '84'}),
                   'snils': forms.TextInput(
                       attrs={'placeholder': '123-456-789 10', 'pattern': "^\d{3}-\d{3}-\d{3} \d{2}$", 'size': 16}),
                   'nom': forms.NumberInput(attrs={'size': 8}),
                   }
        error_messages = {
            'nom': {'unique': 'Формат СНИЛС д.б. 123-456-789 10'}
        }

    def __init__(self, *args, **kwargs):

        super(PdForm, self).__init__(*args, **kwargs)

        self.fields['nom'].error_messages = {
            'unique': ("Номер дела уже используется"),
            'max_digits': ("в номере не должно быть более 8 цифр"),
            'min_value': ("номер не может быть меньше 1")
        }
        self.fields['snils'].error_messages = {
            'invalid': ("СНИЛС не того формата")
        }


    # проверка полей на корректность ввода по правилам ПФР
    def clean(self):
        cleaned_data = super().clean()
        # dhp: datetime = self.cleaned_data['dhp']
        dnp: datetime = self.cleaned_data['dnp']
        dr: datetime = self.cleaned_data['dr']
        ds: datetime = self.cleaned_data['ds']
        dlp: datetime = self.cleaned_data['dlp']
        # nvidp = self.cleaned_data['nvidp']
        zind = self.cleaned_data['zind']
        # nvidp = nvidp.strim()

        if not zind.isdigit():
            raise ValidationError(f"Почтовый индекс должен содержать только цифры, а не Ваше  {zind}")

        '''
        if dhp.year - dlp.year > 20:
            raise ValidationError('Дата хранения больше 20 лет')
        '''
        if dr > datetime.date.today():
            raise ValidationError('Дата рождения в будующем!!!')

        if ds:
            if ds < dnp:
                raise ValidationError('Дата смерти меньше назначения????')
        if dlp < dnp:
            raise ValidationError('Дата прекращеня должна быть больше даты назначения')
        if dlp.day > 1:
            raise ValidationError('Дата прекращеня должна быть первого числа')
            # raise ValidationError('Дата прекращеня должна приходиться на начало месяца')

        return cleaned_data

    def clean_snils(self):
        snils = self.cleaned_data['snils']
        ks_pd = snils[12:14]
        '''Проверка контрольного числа проводится только для номеров 
        больше номера 001-001-998.
        (вот это что-то новое – будет уточнено в ОПФР)
        
        Контрольное число СНИЛС рассчитывается следующим образом:
        * Каждая цифра СНИЛС умножается на номер своей позиции 
          (позиции отсчитываются с конца);
        * Полученные произведения суммируются;
        * Если сумма меньше 100, то контрольное число равно самой сумме;
        * Если сумма равна 100 или 101, то контрольное число равно 00;
        * Если сумма больше 101, то сумма делится нацело на 101 и контрольное число определяется
          остатком от деления аналогично предыдущим двум пунктам.'''
        ks_pfr = 0
        ks_pfr = ks_pfr + 9 * int(snils[0:1])
        ks_pfr = ks_pfr + 8 * int(snils[1:2])
        ks_pfr = ks_pfr + 7 * int(snils[2:3])
        ks_pfr = ks_pfr + 6 * int(snils[4:5])
        ks_pfr = ks_pfr + 5 * int(snils[5:6])
        ks_pfr = ks_pfr + 4 * int(snils[6:7])
        ks_pfr = ks_pfr + 3 * int(snils[8:9])
        ks_pfr = ks_pfr + 2 * int(snils[9:10])
        ks_pfr = ks_pfr + 1 * int(snils[10:11])

        if ks_pfr == 100 or ks_pfr == 101:
            ks_pfr == 0
        elif ks_pfr > 101:
            ks_pfr = ks_pfr % 101

        ks_pfr = str(ks_pfr).rjust(2, '0')

        if ks_pfr != ks_pd:
            raise ValidationError(f"Контрольное число в СНИЛС д.б. {ks_pfr}, а вы написали {ks_pd}")
        return snils

    @property
    def clean_dhp(self):

        dhp: datetime = self.cleaned_data['dhp']
        nvidp = self.cleaned_data['nvidp']
        dlp: datetime = self.cleaned_data['dlp']
        ds: datetime = self.cleaned_data['ds']
        srok = dhp.year - dlp.year
        print(f'{nvidp} срок хранения - {srok} лет')
        print(nvidp)
        if srok < 20:
            print('666666')
            if nvidp == 'Пенсия по возрасту':
                print('true uslovie')
                raise ValidationError(f'Дата хранения у {nvidp} д.б. 20 лет')
            if nvidp == 'qq':
                print('true uslovie qq')
                raise ValidationError(f'Дата хранения у {nvidp} д.б. 10 лет')
            if nvidp == 'Пенсия по потери кормильца':
                raise ValidationError('Дата хранения у Пенсия по потери кормильца д.б. 15 лет')
        return dhp

##input_formats=['%d/%m/%Y'],
