from django.contrib import admin
# Register your models here.
from .models import Pd
from .models import VidPens
from .models import CatPens
from .models import VocUlc
from .models import VocNsp
from .models import VocDistrict

class PdAdmin(admin.ModelAdmin):
    list_display = ('nom','snils','fam','name','fname','dr', 'nvidp')
    list_display_links = ('nom','snils','fam','name','fname')
    search_fields = ('nom','snils','fam','name','fname','dr')

class CatPensAdmin(admin.ModelAdmin):
    list_display = ('id','ncatp')

class VocNspAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class VocUlcAdmin(admin.ModelAdmin):
    list_display = ('kodnsp', 'name')
    list_display_links = ('kodnsp', 'name')


class VocDistrictAdmin(admin.ModelAdmin):
    list_display = ('koddistrict', 'namedistrict',)
    list_display_links = ('koddistrict',)
    search_fields = ('koddistrict', 'namedistrict',)

admin.site.register(Pd, PdAdmin)
#admin.site.register(PdAdmin)
admin.site.register(VidPens)
admin.site.register(CatPens)
admin.site.register(VocNsp)
admin.site.register(VocUlc, VocUlcAdmin, )
admin.site.register(VocDistrict, VocDistrictAdmin,)