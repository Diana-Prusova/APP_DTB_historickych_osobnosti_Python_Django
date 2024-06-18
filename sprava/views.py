"""
Modul obsahuje views pro správu databáze bojovnic. 
V této části aplikace je možné vytvářet, upravovat a mazat záznamy
a také stahovat data o záznamech, které se chystáme smazat.

Tato část aplikace je zaheslovaná. Pro přístup je třeba se přihlásit.
Pro přístupu k mazání dat je třeba být přihlášený jako administrátor.
"""

from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  TemplateView,
                                  FormView,
                                  RedirectView
                                  )
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.functions import Lower
from django.core.exceptions import ValidationError

from bojovnice_app import models
from sprava import forms

# ==========================================================================
# KONTROLA PRÁV
# ==========================================================================

class IsAdminControlMixin(UserPassesTestMixin):
    """
    Mixin pro kontrolu, zda je uživatel administrátor.
    """
    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.error(self.request, 'Pro tuto akci nemáte oprávnění.')
        referer_url = self.request.META.get('HTTP_REFERER', '/')
        return redirect(referer_url)


# ==========================================================================
# INDEX
# ==========================================================================

class IndexSpravaView(LoginRequiredMixin, TemplateView):
    """
    View pro zobrazení úvodní stránky sekce "Správa".
    """
    template_name = 'index_sprava.html'

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: IndexSpravaView')
        return super().dispatch(*args, **kwargs)

# ==========================================================================
# LIST
# ==========================================================================

class StatyAdminListView(LoginRequiredMixin, ListView):
    """
    View pro zobrazení seznamu států v sekci správa.
    """
    model = models.Staty
    template_name = 'list_templates/collective_listing_sprava.html'
    extra_context = {
        'tab_name': 'STÁTY',
        'url_new_object': reverse_lazy('sprava:staty-admin-create')
    }

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: StatyAdminListView')
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        """ Funkce pro získání querysetu upravena tak, aby bylo možné seznam řadit."""
        print('! SPOUŠTÍ SE VIEW: StatyAdminListView - get_queryset')
        queryset = super().get_queryset()
        order_name = self.request.GET.get('order_name')
        order_id = self.request.GET.get('order_id')

        if order_name == 'asc':
            return queryset.order_by(Lower('nazev').asc())
        elif order_name == 'desc':
            return queryset.order_by(Lower('nazev').desc())
        elif order_id == 'asc':
            return queryset.order_by('id')
        elif order_id == 'desc':
            return queryset.order_by('-id')
        else:
            return queryset

class StoletiAdminListView(LoginRequiredMixin, ListView):
    """
    View pro zobrazení seznamu století v sekci správa.
    """
    model = models.Stoleti
    template_name = 'list_templates/collective_listing_sprava.html'
    extra_context = {
        'tab_name': 'STOLETÍ',
        'url_new_object': reverse_lazy('sprava:stoleti-admin-create')
    }

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: StoletiAdminListView')
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        """ Funkce pro získání querysetu upravena tak, aby bylo možné seznam řadit."""
        print('! SPOUŠTÍ SE VIEW: StatyAdminListView - get_queryset')
        queryset = super().get_queryset()
        order_name = self.request.GET.get('order_name')
        order_id = self.request.GET.get('order_id')

        if order_name == 'asc':
            print('!!! jsem v order_name == asc')
            return queryset.order_by(Lower('nazev').asc())
        elif order_name == 'desc':
            print('!!! jsem v order_name == desc')
            return queryset.order_by(Lower('nazev').desc())
        elif order_id == 'asc':
            print('!!! jsem v order_id == asc')
            return queryset.order_by('id')
        elif order_id == 'desc':
            print('!!! jsem v order_id == desc')
            return queryset.order_by('-id')
        else:
            print('!!! jsem v else')
            return queryset


class BojovniceAdminListView(LoginRequiredMixin, ListView):
    """
    View pro zobrazení seznamu bojovnic v sekci správa.
    """
    model = models.Bojovnice
    template_name = 'list_templates/bojovnice_listing_sprava.html'
    extra_context = {
        'tab_name': 'BOJOVNICE',
        'url_new_object': reverse_lazy('sprava:bojovnice-admin-create')
    }
    
    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: BojovniceAdminListView')
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        """ Funkce pro získání querysetu upravena tak, aby bylo možné seznam řadit."""
        print('! SPOUŠTÍ SE VIEW: BojovniceAdminListView - get_queryset')
        queryset = super().get_queryset()
        order_name = self.request.GET.get('order_name')
        order_place = self.request.GET.get('order_place')
        order_id = self.request.GET.get('order_id')

        if order_name == 'asc':
            return queryset.order_by(Lower('jmeno').asc())
        elif order_name == 'desc':
            return queryset.order_by(Lower('jmeno').desc())
        elif order_place == 'asc':
            return queryset.order_by(Lower('uzemi').asc())
        elif order_place == 'desc':
            return queryset.order_by(Lower('uzemi').desc())
        elif order_id == 'asc':
            return queryset.order_by('id')
        elif order_id == 'desc':
            return queryset.order_by('-id')
        else:
            return queryset


class VsechnaJmenaAdminListView(LoginRequiredMixin, ListView):
    """
    View pro zobrazení seznamu tab VsechnaJmena v sekci správa.
    """
    model = models.VsechnaJmena
    template_name = 'list_templates/vsechnajmena_listing_sprava.html'
    extra_context = {
        'tab_name': 'VŠECHNA JMÉNA',
        'url_new_object': reverse_lazy('sprava:vsechna-jmena-admin-create')
    }

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: VsechnaJmenaAdminListView')
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        """ Funkce pro získání querysetu upravena tak, aby bylo možné seznam řadit."""
        print('! SPOUŠTÍ SE VIEW: VsechnaJmenaAdminListView - get_queryset')
        queryset = super().get_queryset()
        order_name = self.request.GET.get('order_name')
        order_ww = self.request.GET.get('order_ww')
        order_id = self.request.GET.get('order_id')

        if order_name == 'asc':
            return queryset.order_by(Lower('jmeno').asc())
        elif order_name == 'desc':
            return queryset.order_by(Lower('jmeno').desc())
        elif order_ww == 'asc':
            return queryset.order_by(Lower('bojovnice__jmeno').asc())
        elif order_ww == 'desc':
            return queryset.order_by(Lower('bojovnice__jmeno').desc())
        elif order_id == 'asc':
            return queryset.order_by('id')
        elif order_id == 'desc':
            return queryset.order_by('-id')
        else:
            return queryset


class SkupinyBojovnicAdminListView(LoginRequiredMixin, ListView):
    """
    View pro zobrazení seznamu skupin bojovnic v sekci správa.
    """
    model = models.SkupinyBojovnic
    template_name = 'list_templates/skupinybojovnic_listing_sprava.html'
    extra_context = {'tab_name': 'SKUPINY BOJOVNIC'}
    extra_context = {
        'tab_name': 'SKUPINY BOJOVNIC',
        'url_new_object': reverse_lazy('sprava:skupiny-bojovnic-admin-create')
    }

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: SkupinyBojovnicAdminListView')
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        """ Funkce pro získání querysetu upravena tak, aby bylo možné seznam řadit."""
        print('! SPOUŠTÍ SE VIEW: SkupinyBojovnicAdminListView - get_queryset')
        queryset = super().get_queryset()
        order_name = self.request.GET.get('order_name')
        order_date = self.request.GET.get('order_date')
        order_place = self.request.GET.get('order_place')
        order_id = self.request.GET.get('order_id')

        if order_name == 'asc':
            return queryset.order_by(Lower('jmeno').asc())
        elif order_name == 'desc':
            return queryset.order_by(Lower('jmeno').desc())
        elif order_date == 'asc':
            return queryset.sorted_by_stoleti(reverse=False)
        elif order_date == 'desc':
            return queryset.sorted_by_stoleti(reverse=True)
        elif order_place == 'asc':
            return queryset.order_by(Lower('stat__nazev').asc())
        elif order_place == 'desc':
            return queryset.order_by(Lower('stat__nazev').desc())
        elif order_id == 'asc':
            return queryset.order_by('id')
        elif order_id == 'desc':
            return queryset.order_by('-id')
        else:
            return queryset

# ==========================================================================
# DETAIL
# ==========================================================================

class StatyAdminDetailView(LoginRequiredMixin, DetailView):
    """
    View pro zobrazení detailu státu v sekci správa.
    """
    model = models.Staty
    template_name = 'detail_templates/stat_detail_sprava.html'
    extra_context = {'title_page': 'STÁT - detail'}

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: StatyAdminDetailView')
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        print('! SPOUŠTÍ SE VIEW: StatyAdminDetailView - get_context_data')
        context = super().get_context_data(**kwargs)
        context['back_to_list_url'] = reverse('sprava:staty-admin-list')
        return context


class StoletiAdminDetailView(LoginRequiredMixin, DetailView):
    """
    View pro zobrazení detailu století v sekci správa.
    """
    model = models.Stoleti
    template_name = 'detail_templates/stoleti_detail_sprava.html'
    extra_context = {'title_page': 'STOLETÍ - detail'}

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: StoletiAdminDetailView')
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        print('! SPOUŠTÍ SE VIEW: StoletiAdminDetailView - get_context_data')
        context = super().get_context_data(**kwargs)
        context['back_to_list_url'] = reverse('sprava:stoleti-admin-list')
        return context


class BojovniceAdminDetailView(LoginRequiredMixin, DetailView):
    """
    View pro zobrazení detailu bojovnice v sekci správa.
    """
    model = models.Bojovnice
    template_name = 'detail_templates/bojovnice_detail_sprava.html'
    extra_context = {'title_page': 'BOJOVNICE - detail'}

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: BojovniceAdminDetailView')
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        print('! SPOUŠTÍ SE VIEW: BojovniceAdminDetailView - get_context_data')
        context = super().get_context_data(**kwargs)
        context['back_to_list_url'] = reverse('sprava:bojovnice-admin-list')
        return context


class VsechnaJmenaAdminDetailView(LoginRequiredMixin, DetailView):
    """
    View pro zobrazení detailu jména z tab VšechnaJména v sekci správa.
    """
    model = models.VsechnaJmena
    template_name = 'detail_templates/vsechnajmena_detail_sprava.html'
    extra_context = {'title_page': 'VŠECHNA JMÉNA - detail'}

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: VsechnaJmenaAdminDetailView')
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        print('! SPOUŠTÍ SE VIEW: VsechnaJmenaAdminDetailView - get_context_data')
        context = super().get_context_data(**kwargs)
        context['back_to_list_url'] = reverse('sprava:vsechna-jmena-admin-list')
        return context


class SkupinyBojovnicAdminDetailView(LoginRequiredMixin, DetailView):
    """
    View pro zobrazení detailu skupiny bojovnic v sekci správa.
    """
    model = models.SkupinyBojovnic
    template_name = 'detail_templates/skupinybojovnic_detail_sprava.html'
    extra_context = {'title_page': 'SKUPINA BOJOVNIC - detail'}

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: SkupinyBojovnicAdminDetailView')
        print('args:', args)
        print('kwargs:', kwargs)
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        print('! SPOUŠTÍ SE VIEW: SkupinyBojovnicAdminDetailView - get_context_data')
        context = super().get_context_data(**kwargs)
        context['back_to_list_url'] = reverse('sprava:skupiny-bojovnic-admin-list')
        return context
    

# ==========================================================================
# CREATE
# ==========================================================================

class StatyAdminCreateView(LoginRequiredMixin, CreateView):
    """
    View pro vytvoření nového státu v sekci správa.
    """
    model = models.Staty
    template_name = 'create_update_sprava.html'
    form_class = forms.StatyAdminForm
    extra_context = {'title_page': 'STÁT - nový záznam'}
    success_url = reverse_lazy('sprava:staty-admin-list')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: StatyAdminCreateView')
        return super().dispatch(*args, **kwargs)


class StoletiAdminCreateView(LoginRequiredMixin, CreateView):
    """
    View pro vytvoření nového století v sekci správa.
    """
    model = models.Stoleti
    template_name = 'create_update_sprava.html'
    form_class = forms.StoletiAdminForm
    extra_context = {'title_page': 'STOLETÍ - nový záznam'}
    success_url = reverse_lazy('sprava:stoleti-admin-list')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: StoletiAdminCreateView')
        return super().dispatch(*args, **kwargs)


class BojovniceAdminCreateView(LoginRequiredMixin, CreateView):
    """
    View pro vytvoření nové bojovnice v sekci správa.
    """
    model = models.Bojovnice
    template_name = 'create_update_sprava.html'
    form_class = forms.BojovniceAdminForm
    extra_context = {'title_page': 'BOJOVNICE - nový záznam'}
    success_url = reverse_lazy('sprava:vsechna-jmena-admin-create')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: BojovniceAdminCreateView')
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        """ Funkce pro zobrazení zprávy po úspěšném uložení formuláře."""
        print('! SPOUŠTÍ SE VIEW: BojovniceAdminCreateView - form_valid')
        response = super().form_valid(form)
        messages.warning(
            self.request,
            'Nezapomeň uložit i další jména bojovnice, pokud nějaké má. (Hlavní jméno bylo uloženo automaticky.)'
        )
        return response


class VsechnaJmenaAdminCreateView(LoginRequiredMixin, CreateView):
    """
    View pro vytvoření nového jména bojovnice v sekci správa.
    """
    model = models.VsechnaJmena
    template_name = 'create_update_sprava.html'
    form_class = forms.VsechnaJmenaAdminForm
    extra_context = {'title_page': 'VŠECHNA JMÉNA - nový záznam'}
    success_url = reverse_lazy('sprava:vsechna-jmena-admin-list')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: VsechnaJmenaAdminCreateView')
        return super().dispatch(*args, **kwargs)


class SkupinyBojovnicAdminCreateView(LoginRequiredMixin, CreateView):
    """
    View pro vytvoření nové skupiny bojovnic v sekci správa.
    """
    model = models.SkupinyBojovnic
    template_name = 'create_update_sprava.html'
    form_class = forms.SkupinyBojovnicAdminForm
    extra_context = {'title_page': 'SKUPINY BOJOVNIC - nový záznam'}
    success_url = reverse_lazy('sprava:skupiny-bojovnic-admin-list')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: SkupinyBojovnicAdminCreateView')
        return super().dispatch(*args, **kwargs)

# ==========================================================================
# UPDATE
# ==========================================================================

class StatyAdminUpdateView(LoginRequiredMixin, UpdateView):
    """
    View pro úpravu státu v sekci správa.
    """
    model = models.Staty
    template_name = 'create_update_sprava.html'
    form_class = forms.StatyAdminForm
    extra_context = {'title_page': 'STÁTY - upravit záznam'}
    success_url = reverse_lazy('sprava:staty-admin-list')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: StatyAdminUpdateView')
        return super().dispatch(*args, **kwargs)

class StoletiAdminUpdateView(LoginRequiredMixin, IsAdminControlMixin, UpdateView):
    """
    View pro úpravu století v sekci správa.
    """
    model = models.Stoleti
    template_name = 'create_update_sprava.html'
    form_class = forms.StoletiAdminForm
    extra_context = {'title_page': 'STOLETÍ - upravit záznam'}
    success_url = reverse_lazy('sprava:stoleti-admin-list')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: StoletiAdminUpdateView')
        return super().dispatch(*args, **kwargs)


class BojovniceAdminUpdateView(LoginRequiredMixin, UpdateView):
    """
    View pro úpravu bojovnice v sekci správa.
    """
    model = models.Bojovnice
    template_name = 'create_update_sprava.html'
    form_class = forms.BojovniceAdminForm
    extra_context = {'title_page': 'BOJOVNICE - upravit záznam'}
    success_url = reverse_lazy('sprava:bojovnice-admin-list')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: BojovniceAdminUpdateView')
        return super().dispatch(*args, **kwargs)


class VsechnaJmenaAdminUpdateView(LoginRequiredMixin, UpdateView):
    """
    View pro úpravu jména bojovnice v sekci správa.
    """
    model = models.VsechnaJmena
    template_name = 'create_update_sprava.html'
    form_class = forms.VsechnaJmenaAdminForm
    extra_context = {'title_page': 'VŠECHNA JMÉNA - upravit záznam'}
    success_url = reverse_lazy('sprava:vsechna-jmena-admin-list')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: VsechnaJmenaAdminUpdateView')
        return super().dispatch(*args, **kwargs)


class SkupinyBojovnicAdminUpdateView(LoginRequiredMixin, UpdateView):
    """
    View pro úpravu skupiny bojovnic v sekci správa.
    """
    model = models.SkupinyBojovnic
    template_name = 'create_update_sprava.html'
    form_class = forms.SkupinyBojovnicAdminForm
    extra_context = {'title_page': 'SKUPINY BOJOVNIC - upravit záznam'}
    success_url = reverse_lazy('sprava:skupiny-bojovnic-admin-list')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: SkupinyBojovnicAdminUpdateView')
        return super().dispatch(*args, **kwargs)

# ==========================================================================
# DELETE
# ==========================================================================

class StatyAdminDeleteView(LoginRequiredMixin, IsAdminControlMixin, DeleteView):
    """
    View pro smazání státu v sekci správa.
    Tato akce se zobrazí pouze administrátorovi.
    """
    model = models.Staty
    template_name = 'delete_templates/stat_delete_sprava.html'
    extra_context = {'title_page': 'STÁT - smazání záznamu'}
    success_url = reverse_lazy('sprava:staty-admin-list')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: StatyAdminDeleteView')
        return super().dispatch(*args, **kwargs)


class StoletiAdminDeleteView(LoginRequiredMixin, IsAdminControlMixin, DeleteView):
    """
    View pro smazání století v sekci správa.
    Tato akce se zobrazí pouze administrátorovi.
    """
    model = models.Stoleti
    template_name = 'delete_templates/stoleti_delete_sprava.html'
    extra_context = {'title_page': 'STOLETÍ - smazání záznamu'}
    success_url = reverse_lazy('sprava:stoleti-admin-list')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: StoletiAdminDeleteView')
        return super().dispatch(*args, **kwargs)


class BojovniceAdminDeleteView(LoginRequiredMixin, IsAdminControlMixin, DeleteView):
    """
    View pro smazání bojovnice v sekci správa.
    Tato akce se zobrazí pouze administrátorovi.
    """
    model = models.Bojovnice
    template_name = 'delete_templates/bojovnice_delete_sprava.html'
    extra_context = {'title_page': 'BOJOVNICE - smazání záznamu'}
    success_url = reverse_lazy('sprava:bojovnice-admin-list')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: BojovniceAdminDeleteView')
        return super().dispatch(*args, **kwargs)


class VsechnaJmenaAdminDeleteView(LoginRequiredMixin, IsAdminControlMixin, DeleteView):
    """
    View pro smazání jména z tab VšechnaJména v sekci správa.
    Tato akce se zobrazí pouze administrátorovi.
    """
    model = models.VsechnaJmena
    template_name = 'delete_templates/vsechnajmena_delete_sprava.html'
    extra_context = {'title_page': 'VŠECHNA JMÉNA - smazání záznamu'}
    success_url = reverse_lazy('sprava:vsechna-jmena-admin-list')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: VsechnaJmenaAdminDeleteView')
        return super().dispatch(*args, **kwargs)


class SkupinyBojovnicAdminDeleteView(LoginRequiredMixin, IsAdminControlMixin, DeleteView):
    """
    View pro smazání skupiny bojovnic v sekci správa.
    Tato akce se zobrazí pouze administrátorovi.
    """
    model = models.SkupinyBojovnic
    template_name = 'delete_templates/skupinybojovnic_delete_sprava.html'
    extra_context = {'title_page': 'SKUPINY BOJOVNIC - smazání záznamu'}
    success_url = reverse_lazy('sprava:skupiny-bojovnic-admin-list')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: SkupinyBojovnicAdminDeleteView')
        return super().dispatch(*args, **kwargs)

# ==========================================================================
# DOWLAND
# ==========================================================================

class DownloadDataView(LoginRequiredMixin, TemplateView):
    """
    View pro stažení kompletních dat o objektu (detail + propojení),
    který se administrátor chystá smazat.
    """
    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: SkupinyBojovnicAdminDeleteView')
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: SkupinyBojovnicAdminDeleteView - get')
        model = request.GET.get('model')
        pk = request.GET.get('id')

        try:
            if model == 'staty':
                context = models.Staty.objects.get(pk=pk)
            elif model == 'stoleti':
                context = models.Stoleti.objects.get(pk=pk)
            elif model == 'bojovnice':
                context = models.Bojovnice.objects.get(pk=pk)
            elif model == 'vsechnajmena':
                context = models.VsechnaJmena.objects.get(pk=pk)
            elif model == 'skupinybojovnic':
                context = models.SkupinyBojovnic.objects.get(pk=pk)

        except models.Staty.DoesNotExist:
            messages.error(request, 'Soubor s daty se nepodařilo uložit.')
            return redirect('sprava:staty-admin-delete', pk=kwargs['pk'])
        
        data = context.get_data()

        response = HttpResponse(data, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename=data_{model}_{pk}.txt'
        return response

# ==========================================================================
# LOGIN
# ==========================================================================

class LoginView(FormView):
    """ View pro přihlášení."""
    form_class = forms.MyAuthenticationForm
    template_name = 'login_template.html'

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: LoginView')
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        print('! SPOUŠTÍ SE VIEW: LoginView - form_valid')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')       
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(reverse('sprava:index-sprava'))
        return super().form_valid(form)


class LogoutView(RedirectView):
    """ View pro odhlášení."""
    url = reverse_lazy('sprava:login')

    def dispatch(self, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: LogoutView')
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        print('! SPOUŠTÍ SE VIEW: LogoutView - get')
        logout(request)
        return super().get(request, *args, **kwargs)



    