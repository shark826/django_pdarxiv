from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
from django.core import paginator
from django.db.models.base import Model
from django.db.models import Q 
from django.views.generic.detail import DetailView
from pdarxiv.models import Pd, VidPens

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
        #c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()))
                #+ list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_view(request):
    logout(request)
    #template = loader.get_template('/')
    return HttpResponseRedirect(reverse_lazy('home'))

    #return HttpResponse(template.render())

### Главный экран, поиск и добавление дел
'''
class PdList(ListView):
    model = Pd
    template_name = 'pdarxiv/index.html'
    #context_object_name = 'pds'
    paginate_by = 15


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allrec'] = Pd.objects.all()
        filtered_persons = PdFilter(self.request.GET,
                                    queryset=self.get_queryset().order_by('nom'))
        context['filter'] = filtered_persons
        paginated_filtered_persons = Paginator(filtered_persons.qs, 15)
        print(paginated_filtered_persons.num_pages)
        page_number = self.request.GET.get('page')
        print(page_number)
        person_page_obj = paginated_filtered_persons.get_page(page_number)
        #context['person_page_obj'] = person_page_obj
        context['pds'] = person_page_obj
        return context
'''
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
    print(paginated_filtered_persons.count)
    page_number = request.GET.get('page')
    print(page_number)
    person_page_obj = paginated_filtered_persons.get_page(page_number)

    context['person_page_obj'] = person_page_obj
    return render(request,'pdarxiv/index.html',context=context)


### Формирование оиписи выплатных дел с истекшим сроком хранения, подлежащих уничтожению
class PdListDestroy(ListView):
    model = Pd
    template_name = 'pdarxiv/index-destroy.html'
    context_object_name = 'pdsd'
    
    #p = Paginator (pdsd, 15)
    #paginate_by = 35
    #filterset_class = PdFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filter'] = PdFilterDestroy(self.request.GET, 
                                            queryset=self.get_queryset())
        paginator = Paginator(filter, 15)
        

        page = self.request.GET.get('page')
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)    
        return context


class PdSearch(ListView):
    model = Pd
    template_name = 'pdarxiv/PdSearch.html'
    


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #print(context)
        context ['filter'] = PdFilter(self.request.GET, queryset=self.get_queryset())
        return context

### Добавление архдела
class PdCreateView(CreateView):
    template_name = 'pdarxiv/create.html'
    context_object_name = 'arxdelo'
    form_class = PdFormC
    success_url = reverse_lazy('arxpd')


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
class PdUpdateView(UpdateView):
    model = Pd
    template_name = 'pdarxiv/create.html'
    '''
    fields = ['snils', 'nom', 'fam', 'name', 'fname',
    'dr', 'ds', 'zind', 'gor', 'ul', 'dom', 'kor', 'kvar', 
    'dnp', 'dlp', 'dhp', 'drr', 'post',
    'link', 'sud', 'nud', 'nvidp']
    '''
    form_class = PdForm
    context_object_name = 'arxdelo'
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('viewarxpd', args = (self.object.id,))

### Удаление архдела
class PdDeleteView(DeleteView):
    model = Pd
    template_name = 'pdarxiv/delete-arxdelo.html'
    context_object_name = 'arxdelo'
    success_url = reverse_lazy('arxpd')


def my_search(request):

    # BTW you do not need .all() after a .filter()
    # local_url.objects.filter(global_url__id=1) will do
    filtered_qs = filters.PdFilterDestroy(
                      request.GET,
                      queryset=Pd.objects.all()
                  ).qs
    print(filtered_qs)
    paginator = Paginator(filtered_qs, 10)

    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    return render(
        request,
        'pdarxiv/search.html',
        {'response': response}
    )


class FilteredListView(ListView):
    filterset_class = None

    def get_queryset (self):
        # Get the queryset however you usually would. For example:
        queryset = super().get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return 