import django_filters
from django.forms import DateInput, TextInput, IntegerField
from django_filters.widgets import RangeWidget

from .models import Pd

class PdFilter (django_filters.FilterSet):
    #paginate_by = 35

    nom = django_filters.CharFilter(field_name='nom', lookup_expr='icontains', label='',
                                      widget=TextInput(attrs={'placeholder': 'Номер дела',
                                                              'type':'number', 'min':'1',
                                                              'data-mask':"00000000",
                                                              "style":"margin:0.5rem 0 0 0",}))
    snils = django_filters.CharFilter(field_name='snils', lookup_expr='exact', label="",
                                    widget=TextInput(attrs={"placeholder": "000-000-000 00",
                                                            "data-mask":"000-000-000 00",
                                                            "style":"margin:0.5rem 0 0 0",}))
    fam = django_filters.CharFilter(field_name='fam', lookup_expr='istartswith', label='',
                                     widget=TextInput(attrs={'placeholder': 'Фамилия',
                                                             "style":"margin:0.5rem 0 0 0",}))
    name = django_filters.CharFilter(field_name='name', lookup_expr='istartswith', label='',
                                     widget=TextInput(attrs={'placeholder': 'Имя',
                                                             "style":"margin:0.5rem 0 0 0",}))
    fname = django_filters.CharFilter(field_name='fname', lookup_expr='istartswith', label='',
                                     widget=TextInput(attrs={'placeholder': 'Отчество',
                                                             "style":"margin:0.5rem 0 0 0",}))
    class Meta:
        model = Pd

        fields = {
            #'nom': ['icontains'],
            #'snils': ['exact'],
            #'fam': ['istartswith'],
            #'name': ['istartswith'],
            #'fname': ['istartswith'],
            'nvidp': ['exact'],
        }

class PdFilterDestroy (django_filters.FilterSet):
    #snils = django_filters.CharFilter(field_name='snils', lookup_expr='exact', label='',
    #                                  widget=TextInput(attrs={"placeholder": "000-000-000 00",
    #                                                         "data-mask": "000-000-000 00", }))
    start_date = django_filters.DateFilter(field_name='dhp', lookup_expr=('gte'),
                                           label='Дата хранения:  С',
                                           widget=TextInput(attrs={'placeholder': 'ДД.ММ.ГГГГ', 'type':'date',
                                                                   'required': 'true'}))
    end_date = django_filters.DateFilter(field_name='dhp', lookup_expr=('lte'),
                                         label='Дата хранения:  ПО',
                                         widget=TextInput(attrs={'placeholder': 'ДД.ММ.ГГГГ', 'type':'date',
                                                                 'required': 'true'}))

    class Meta:
        model = Pd
        paginate_by = 35
        fields = {
          #  'nom': ['icontains'],
          #  'snils': ['exact'],
            'nvidp':['exact'],


        }