from ajax_select import register, LookupChannel
from .models import Pd
from django.utils.html import escape

#@register('gor')
class PdLookup(LookupChannel):

    model = Pd

    def get_query(self, q, request):
        return self.model.objects.filter(gor__icontains=q).order_by('name')[:15]

    def get_result(self, obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.name

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return escape(obj.name)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return escape(obj.name)

    