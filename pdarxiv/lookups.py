from ajax_select import register, LookupChannel
from .models import Pd


@register('gor')
class PdLookup(LookupChannel):

    model = Pd

    def get_query(self, q, request):
        return self.model.objects.filter(gor__icontains=q).order_by('name')[:15]
    
    def format_item_display(self, form):
        return u"<span class='tag'>%s</span>" % form.gor

    