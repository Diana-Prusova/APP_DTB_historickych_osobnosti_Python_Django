"""
Views pro aplikaci bojovnice_app slouží k zobrazení dat pro uživatelskou 
část aplikace. Zde zobrazená data jsou přístupná všem uživatelům a v této
části aplikace je není možné jakkoliv editovat.

Views jsou napojena do urls.py v kořenovém adresáři (tedy bojovnice_v_historii).
"""

from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView
)
from bojovnice_app import models
from bojovnice_app import forms
from django.db.models.functions import Lower

# ==========================================================================
# LIST 
# ==========================================================================

class BojovniceAppIndexView(TemplateView):
    """
    View pro zobrazení úvodní stránky uživatelské části aplikace (bojovnice_app).
    Toto view obsahuje:
    - možnosti zobrazení kompletního seznamu bojovnic
    - možnosti zobrazení kompletního seznamu skupin bojovnic
    - formulář pro vyhledávání bojovnic a skupin bojovnic podle státu
    - formulář pro vyhledávání bojovnic a skupin bojovnic podle století
    - formulář pro vyhledávání bojovnic a skupin bojovnic podle jména
    """

    template_name = 'index_bojovnice_app.html'
    success_url = 'listing_bojovnice_app.html'
    search_by_stat_form = forms.SearchByStatForm()
    search_by_stoleti_form = forms.SearchByStoletiForm()
    search_by_vsechna_jmena_form = forms.SeachByVsechnaJmenaForm()


    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: IndexBojovniceAppView')
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        print('! SPOUŠTÍ SE VIEW: IndexBojovniceAppView - get_context_data')
        context = super().get_context_data(**kwargs)
        context['search_by_stat_form'] = self.search_by_stat_form
        context['search_by_stoleti_form'] = self.search_by_stoleti_form
        context['search_by_vsechna_jmena_form'] = self.search_by_vsechna_jmena_form
        context['data'] = models.BojovniceStat.objects.all().get_maps_data()
        return context
    
    def post(self, request, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: IndexBojovniceAppView - post')

        if 'stat' in request.POST:
            data = models.Staty.objects.get(pk=request.POST['stat']).get_all_connect_obj()
        elif 'stoleti' in request.POST:
            data = models.Stoleti.objects.get(pk=request.POST['stoleti']).get_all_connect_obj()
        elif 'jmeno' in request.POST:
            bojovnice = models.Bojovnice.objects.search_by_text(request.POST['jmeno'])
            skupiny_bojovnic = models.SkupinyBojovnic.objects.filter(jmeno__icontains=request.POST['jmeno'])
            data = list(bojovnice) + list(skupiny_bojovnic)
        else:
            return render(
                request,
                template_name='error_template_bojovnice_app.html',
                )

        return render(
            request,
            template_name='listing_search_bojovnice_app.html',
            context={
                'object_list': data
            })


class BojovniceAppListBojovniceView(ListView):
    """
    View pro zobrazení kompletního seznamu bojovnic.
    """
    model = models.Bojovnice
    template_name = 'listing_bojovnice_app.html'
    extra_context = {
        'title_page': 'SEZNAM BOJOVNIC'
    }

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: BojovniceAppListBojovniceView')
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        """
        Funkce pro získání querysetu. Je upravená tak, aby bylo možné
        zobrazený seznam řadit podle jména a podle století.
        """
        print('! SPOUŠTÍ SE VIEW: BojovniceAppListBojovniceView - get_queryset')
        queryset = super().get_queryset()
        order_name = self.request.GET.get('order_name')
        order_date = self.request.GET.get('order_date')

        if order_name == 'asc':
            return queryset.order_by(Lower('jmeno').asc())
        elif order_name == 'desc':
            return queryset.order_by(Lower('jmeno').desc())
        elif order_date == 'asc':
            return queryset.sorted_by_stoleti(reverse=False)
        elif order_date == 'desc':
            return queryset.sorted_by_stoleti(reverse=True)
        else:
            return queryset
    
class BojovniceAppListSkupinyBojovnicView(ListView):
    """
    View pro zobrazení kompletního seznamu skupin bojovnic.
    """
    model = models.SkupinyBojovnic
    template_name = 'listing_bojovnice_app.html'
    extra_context = {
        'title_page': 'SEZNAM SKUPIN BOJOVNIC'
    }

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: BojovniceAppListSkupinyBojovnicView')
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        """
        Funkce pro získání querysetu. Je upravená tak, aby bylo možné
        zobrazený seznam řadit podle jména a podle století.
        """
        print('! SPOUŠTÍ SE VIEW: BojovniceAppListSkupinyBojovnicView - get_queryset')
        queryset = super().get_queryset()
        order_name = self.request.GET.get('order_name')
        order_date = self.request.GET.get('order_date')

        if order_name == 'asc':
            return queryset.order_by(Lower('jmeno').asc())
        elif order_name == 'desc':
            return queryset.order_by(Lower('jmeno').desc())
        elif order_date == 'asc':
            return queryset.sorted_by_stoleti(reverse=False)
        elif order_date == 'desc':
            return queryset.sorted_by_stoleti(reverse=True)
        else:
            return queryset

# ==========================================================================
# DETAIL 
# ==========================================================================

class BojovniceAppDetailBojovniceView(DetailView):
    """
    View pro zobrazení detailu bojovnice.
    """
    model = models.Bojovnice
    template_name = 'detail_templates_app/detail_one_bojovnice_app.html'

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: BojovniceDetailView')
        return super().dispatch(*args, **kwargs)

class BojovniceAppDetailSkupinyBojovnicView(DetailView):
    """
    View pro zobrazení detailu jedné skupiny bojovnic.
    """
    model = models.SkupinyBojovnic
    template_name = 'detail_templates_app/detail_group_bojovnice_app.html'

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: BojovniceDetailView')
        return super().dispatch(*args, **kwargs)