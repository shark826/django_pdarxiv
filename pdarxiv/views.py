from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView, redirect_to_login
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core import paginator

from django.db.models.base import Model
from django.db.models import Q 
from django.views.generic.detail import DetailView
from pdarxiv.models import Pd, VidPens, VocNsp, VocUlc
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from . import filters
from .forms import PdFormC, PdForm
from .filters import PdFilter, PdFilterDestroy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def index0(request):
    template = loader.get_template('pdarxiv/home.html')

    return HttpResponse(template.render())


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'pdarxiv/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        return dict(list(context.items()))


    def get_success_url(self):
        return reverse_lazy('home')

def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse_lazy('home'))



### Главный экран, поиск и добавление дел

def PdList(request):
    context = {}
    all_reccords = Pd.objects.all().count()
    filtered_persons =  PdFilter(
        request.GET,
        queryset = Pd.objects.all().order_by('fam', 'name', 'fname')
    )
    context['allrec'] = all_reccords
    context['filter'] = filtered_persons

    paginated_filtered_persons = Paginator(filtered_persons.qs, 20)
    page_number = request.GET.get('page')
    person_page_obj = paginated_filtered_persons.get_page(page_number)

    context['person_page_obj'] = person_page_obj
    return render(request,'pdarxiv/index.html',context=context)


### Формирование оиписи выплатных дел с истекшим сроком хранения, подлежащих уничтожению
class PdListDestroy(ListView):
    model = Pd
    template_name = 'pdarxiv/index-destroy.html'
    context_object_name = 'pdsd'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filter'] = PdFilterDestroy(self.request.GET, 
                                            queryset=self.get_queryset())

        return context


### Добавление архдела
class PdCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'pdarxiv/create.html'
    context_object_name = 'arxdelo'
    form_class = PdFormC
    success_url = reverse_lazy('arxpd')
    permission_required = 'pdarxiv.add_pd'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vidp'] = VidPens.objects.all()

        return context


### Просмотр архдела
class PdDetailView(DetailView):
    model = Pd
    template_name = 'pdarxiv/arxdelo.html'
    context_object_name = 'arxdelo'
    

### Редактирование архдела
class PdUpdateView(PermissionRequiredMixin, UpdateView):
    model = Pd
    template_name = 'pdarxiv/create.html'

    form_class = PdForm
    context_object_name = 'arxdelo'

    permission_required = 'pdarxiv.change_pd'
    permission_denied_message = 'Hooo!'


    def get_success_url(self, **kwargs):         
        return reverse_lazy('viewarxpd', args = (self.object.id,))

### Удаление архдела
class PdDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'pdarxiv.delete_pd'
    permission_denied_message = 'it`s not your business'

    model = Pd
    template_name = 'pdarxiv/delete-arxdelo.html'
    context_object_name = 'arxdelo'
    success_url = reverse_lazy('arxpd')

    def handle_no_permission(self):
        messages.error(self.request, 'You dont have permission to do this')
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

### справочник городов

def load_cities(request):
    city = VocNspo.objects.all()
    d = {'city': city}
    return render(request,'create.html',d)

### Справочник улиц
def load_streets(request):
    kodnsp_id = request.GET.get('kodnsp')
    streets = VocUlc.objects.filter(kodnsp_id=kodnsp_id).order_by('name')
    return render(request, 'streets_dropdown_list_options.html', {'streets': streets})