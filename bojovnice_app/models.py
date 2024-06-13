"""
Modul obsahuje modely pro celou aplikaci. Zde je nastavena struktura
databáze, včetně vztahů mezi tabulkami a vlastností jednotlivých polí.
Do všech ostatních aplikací jsou tyto modely importovány.
"""

from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib import messages
from django.core.exceptions import ValidationError


# ==========================================================================
# TVORBA QUERYSETŮ
# ==========================================================================

class BojovniceQuerySet(models.QuerySet):
    def search_by_text(self, text):
        """
        Funkce pro vyhledávání bojovnic podle jména. Prohledá tabulku VšechnaJmena
        a vrátí všechny bojovnice, jejichž jméno obsahuje zadaný text. Pokud žádná 
        bojovnice neodpovídá, vrátí prázdný queryset.
        :param text: text, podle kterého se vyhledává    
        """
        matching_names = VsechnaJmena.objects.filter(jmeno__icontains=text)
        return self.filter(vsechnajmena__in=matching_names).distinct()

    def sorted_by_stoleti(self, reverse):
        """
        Vrátí queryset seřazený podle století. 
        :param reverse: True - sestupně, False - vzestupně
        """
        my_query = sorted(self, key=lambda x: x.stoleti.first().pk, reverse=reverse)
        return my_query
    

class BojovniceManager(models.Manager):
    def get_queryset(self):
        return BojovniceQuerySet(self.model, using=self._db)
    
    def search_by_text(self, text):
        return self.get_queryset().search_by_text(text)
    
    def sorted_by_stoleti(self, reverse):
        return self.get_queryset().sorted_by_stoleti(reverse)
    

class SkupinyBojovnicQuerySet(models.QuerySet):
    def sorted_by_stoleti(self, reverse):
        """
        Vrátí queryset seřazený podle století. 
        :param reverse: True - sestupně, False - vzestupně
        """
        my_query = sorted(self, key=lambda x: x.get_num_for_sort_by_stoleti(), reverse=reverse)
        return my_query
    
    
class SkupinyBojovnicManager(models.Manager):
    def get_queryset(self):
        return SkupinyBojovnicQuerySet(self.model, using=self._db)
    
    def sorted_by_stoleti(self, reverse):
        return self.get_queryset().sorted_by_stoleti(reverse)    

# ==========================================================================
# TVORBA GENERICKÝCH TŘÍD
# ==========================================================================

class Data():
    """
    Rodičovnský objekt pro všechny modely. Obsahuje metody pro získání
    a zobrazení dat objektu, včetně informace o napojených objektech.
    """
    def get_data(self):
        """
        Vrátí data instance včetně informace o napojených instancích
        ve formátu string.
        """
        return NotImplementedError('Nebyla implementována metoda get_data().')
    
    def print_data(self):
        """
        Vrátí data instance formátované do konzole.
        """
        print("=" * 50)
        print(self.get_data())
        print("=" * 50)

    def save_data(self):
        """
        Zapíše a uloží data instance do souboru ve formátu .txt.
        """
        actual_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
        file_name = f"{self.__class__.__name__}_{self.pk}_{actual_time}.txt"
        with open(file_name, mode='w', encoding='utf-8') as file:
            file.write(self.get_data())

# ==========================================================================
# TVORBA MODELŮ
# ==========================================================================

class Staty(models.Model, Data):
    nazev = models.CharField(max_length=50)

    class Meta:
        ordering = ('nazev',) # způsob řazen
        verbose_name_plural = 'Státy' # název v django adminu (smaže 's' na konci)

    def __str__(self):
        """Zobrazení pro rolovací menu."""
        return f"{self.nazev}"
    
    @property
    def admin_string(self):
        """Zobrazení pro administraci."""
        return f"{self.nazev} (ID: {self.pk})"
    
    def get_data(self):
        """Kompletní výpis informací včetně napojených objektů."""
        data = f'STÁT: {self.nazev}'
        data += "\nNAPOJENÉ BOJOVNICE:"
        if self.bojovnice_set.count() == 0:
            data += "\n- stát není napojen na žádné bojovnice"
        else:
            for each in self.bojovnice_set.all():
                data += f"- {each.admin_string}\n"
        data += "\nNAPOJENÉ SKUPINY BOJOVNIC:\n"
        if self.skupinybojovnic_set.count() == 0:
            data += "\n- stát není napojen na žádné skupiny bojovnic"
        else:
            for each in self.skupinybojovnic_set.all():
                data += f"- {each.admin_string}\n"
        return data
    
    def get_all_connect_obj(self):
        """ 
        Vrátí všechny navázané instance z tabulek Bojovnice 
        a Skupiny bojovnic.
        """
        bojovnice = Bojovnice.objects.filter(stat=self)
        skupiny_bojovnic = SkupinyBojovnic.objects.filter(stat=self)
        all_objects = list(bojovnice) + list(skupiny_bojovnic)
        return sorted(all_objects, key=lambda x: x.jmeno)

    def get_absolute_url_detail(self):
        """Vrátí URL adresu detailu instance pro podaplikaci správy."""
        return reverse('sprava:staty-admin-detail', kwargs={'pk': self.pk})
    
    def get_absolute_url_update(self):
        """Vrátí URL adresu stránky, kde je možné instanci upravit. """
        return reverse('sprava:staty-admin-update', kwargs={'pk': self.pk})
    
    def get_absolute_url_delete(self):
        """Vrátí URL adresu stránky, kde je možné instanci instanci smazat z DTB. """
        return reverse('sprava:staty-admin-delete', kwargs={'pk': self.pk})
    
    
class Stoleti(models.Model, Data):
    nazev = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Století' # název v django adminu

    def __str__(self):
        """Zobrazení pro rolovací menu."""
        return f"{self.nazev}"
    
    @property
    def admin_string(self):
        """Zobrazení pro administraci."""
        return f"{self.nazev} (ID: {self.pk})"
    
    def get_data(self):
        """Kompletní výpis informací o instanci včetně napojených objektů."""
        data = f'STOLETÍ: {self.nazev}'
        data += "\nNAPOJENÉ BOJOVNICE:"
        if self.bojovnice_set.count() == 0:
            data += "\n- století není napojeno na žádné bojovnice"
        else:
            for each in self.bojovnice_set.all():
                data += f"- {each.admin_string}\n"
        data += "\nNAPOJENÉ SKUPINY BOJOVNIC:\n"
        if self.skupinybojovnic_set.count() == 0:
            data += "\n- století není napojeno na žádné skupiny bojovnic"
        else:
            for each in self.skupinybojovnic_set.all():
                data += f"- {each.admin_string}\n"
        return data
    
    def get_all_connect_obj(self):
        """ 
        Vrátí všechny navázané objekty z tabulek Bojovnice 
        a Skupiny bojovnic.
        """
        bojovnice = Bojovnice.objects.filter(stoleti=self)
        skupiny_bojovnic = SkupinyBojovnic.objects.filter(stoleti=self)
        return list(bojovnice) + list(skupiny_bojovnic)
    
    def get_absolute_url_detail(self):
        """Vrátí URL adresu detailu instance pro podaplikaci správy."""
        return reverse('sprava:stoleti-admin-detail', kwargs={'pk': self.pk})
    
    def get_absolute_url_update(self):
        """Vrátí URL adresu stránky, kde je možné instanci upravit. """
        return reverse('sprava:stoleti-admin-update', kwargs={'pk': self.pk})
    
    def get_absolute_url_delete(self):
        """Vrátí URL adresu stránky, kde je možné instanci instanci smazat z DTB. """
        return reverse('sprava:stoleti-admin-delete', kwargs={'pk': self.pk})
    
    
class Bojovnice(models.Model, Data):
    jmeno = models.CharField(max_length=50)
    obdobi = models.CharField(max_length=50) 
    uzemi = models.CharField(max_length=50) 
    popis = models.TextField(max_length=100) 
    pribeh = models.TextField(max_length=2000)
    stat = models.ManyToManyField(Staty)
    stoleti = models.ManyToManyField(Stoleti)

    objects = BojovniceManager() # vlastní manager

    class Meta:
        ordering = ('jmeno',) # způsob řazení
        verbose_name_plural = 'Bojovnice' # název v django adminu

    def __str__(self):
        """Zobrazení pro rolovací menu."""
        return f"{self.jmeno} | {self.uzemi}"
    
    @property
    def admin_string(self):
        """Zobrazení pro administraci."""
        return f"{self.jmeno} (ID: {self.pk}) | {self.uzemi} | {self.obdobi}"
    
    @property
    def staty_string(self):
        """Zobrazení seznamu napojených státu jako string."""
        all_staty = self.stat.all()
        if all_staty:
            return ', '.join([stat.nazev for stat in all_staty])
        else:
            return 'Není přiřazen žádný stát.'
        
    @property
    def stoleti_string(self):
        """Zobrazení seznamu napojených století jako string."""
        all_stoleti = self.stoleti.all()
        if all_stoleti:
            return ', '.join([stoleti.nazev for stoleti in all_stoleti])
        else:
            return 'Není přiřazeno žádné století.'
        
    @property
    def vsechna_jmena_string(self):
        """
        Funkce prohledá tabulku VsechnaJmena a najde všechna jména přiřazená
        k dané bojovnici. Vrátí je jako string. Pokud má bojovnice pouze jedno
        jméno, vrátí False.
        """
        jmena = self.vsechnajmena_set.all()
        if jmena == 1:
            return False
        else:
            return ', '.join([jmeno.jmeno for jmeno in jmena])
        
    @property
    def vedlejsi_jmena_string(self):
        """
        Funkce prohledá tabulku VsechnaJmena a vytvoří seznam všech jmen bojovnice.
        Následně odstraní jméno, které je použito jako hlavní jméno a ostatní
        vrátí jako string. Pokud má bojovnice pouze jedno jméno, vrátí False.
        """
        jmena = [jmeno.jmeno for jmeno in self.vsechnajmena_set.all()]
        jmena.remove(self.jmeno)
        if jmena:
            return ', '.join(jmena)
        else:
            return False

    def save(self, *args, **kwargs):
        """
        Přepsaná metoda pro uložení instance, tak aby se při ukládání
        automaticky uložilo jméno bojovnice do tabulky VsechnaJmena
        a zároveň jej nastaví jako hlavní (tedy nesmazatelné).
        """
        new_instance = self.pk is None
        super().save(*args, **kwargs)
        if new_instance:
            VsechnaJmena.objects.create(jmeno=self.jmeno, bojovnice=self, hlavni_jmeno=True)
        
    def get_data(self):
        """Kompletní výpis informací o instanci."""
        data = f'BOJOVNICE: {self.jmeno}'
        data += f"\n- POPIS: {self.popis}"
        data += f"\n- OBDODÍ: {self.obdobi}"
        data += f"\n- ÚZEMÍ: {self.uzemi}"
        data += f"\n- NAPOJENÉ STÁTY: {self.staty_string}"
        data += f"\n- NAPOJENÁ STOLETÍ: {self.stoleti_string}"
        data += f"\n- VŠECHNA JMÉNA: {self.vsechna_jmena_string}"
        data += f"\n- PŘÍBĚH: {self.pribeh}"
        return data
        
    def get_absolute_url_detail(self):
        """Vrátí URL adresu detailu instance pro podaplikaci správy."""
        return reverse('sprava:bojovnice-admin-detail', kwargs={'pk': self.pk})

    def get_absolute_url_update(self):
        """Vrátí URL adresu stránky, kde je možné instanci upravit. """
        return reverse('sprava:bojovnice-admin-update', kwargs={'pk': self.pk})
    
    def get_absolute_url_delete(self):
        """Vrátí URL adresu stránky, kde je možné instanci instanci smazat z DTB. """
        return reverse('sprava:bojovnice-admin-delete', kwargs={'pk': self.pk})
    
    def get_absolute_url_bojovnice_app(self):
        """Vrátí URL adresu detailu instance pro uživatelskou část aplikace."""
        return reverse('one_detail_bojovnice_app', kwargs={'pk': self.pk})
    
    def is_bojovnice(self):
        """Slouží k rozlišení modelů v template listing pro bojovnice APP """
        return True
    
    
class VsechnaJmena(models.Model):
    jmeno = models.CharField(max_length=50)
    bojovnice = models.ForeignKey(Bojovnice, on_delete=models.CASCADE)
    hlavni_jmeno = models.BooleanField(default=False)

    class Meta:
        ordering = ('bojovnice', 'jmeno',) # způsob řazen
        verbose_name_plural = 'Všechna jména' # název v django adminu

    def __str__(self):
        """Zobrazení pro vývojáře v administraci."""
        return f"{self.jmeno}"
    
    @property
    def admin_string(self):
        """Zobrazení pro administraci."""
        return f"{self.jmeno} (ID: {self.pk}) |  BOJOVNICE: {self.bojovnice.jmeno} (ID {self.bojovnice.pk}), {self.bojovnice.uzemi}"

    def delete(self, *args, **kwargs):
        """
        Přepsaná metoda pro smazání instance, tak aby se 
        nedalo smazat hlavní jméno.
        """
        if self.hlavni_jmeno:
            print('!!!Nelze smazat hlavní jméno bojovnice.')
        else:
            super().delete(*args, **kwargs)

    def get_data(self):
        """Kompletní výpis informací o objektu."""
        data = f'JMÉNO: {self.jmeno}'
        data += f"\n- BOJOVNICE: {self.bojovnice.admin_string}"
        return data
    
    def get_absolute_url_detail(self):
        """Vrátí URL adresu detailu instance pro podaplikaci správy."""
        return reverse('sprava:vsechna-jmena-admin-detail', kwargs={'pk': self.pk})
   
    def get_absolute_url_update(self):
        """Vrátí URL adresu stránky, kde je možné instanci upravit. """
        return reverse('sprava:vsechna-jmena-admin-update', kwargs={'pk': self.pk})
    
    def get_absolute_url_delete(self):
        """Vrátí URL adresu stránky, kde je možné instanci instanci smazat z DTB. """
        return reverse('sprava:vsechna-jmena-admin-delete', kwargs={'pk': self.pk})


class SkupinyBojovnic(models.Model, Data):
    jmeno = models.CharField(max_length=50)
    popis = models.TextField(max_length=5000)
    stat = models.ManyToManyField(Staty, blank=True)
    stoleti = models.ManyToManyField(Stoleti, blank=True)
    bojovnice = models.ManyToManyField(Bojovnice, blank=True)

    objects = SkupinyBojovnicManager()

    class Meta:
        ordering = ('jmeno',) # způsob řazen
        verbose_name_plural = 'Skupiny bojovnic' # název v django adminu

    def __str__(self):
        """Zobrazení pro vývojáře v administraci."""
        return f"{self.jmeno}"
    
    @property
    def admin_string(self):
        """Zobrazení pro administraci."""
        staty_string = ', '.join([stat.nazev for stat in self.stat.all()])
        return f"{self.jmeno}  |  ID: {self.pk}  |  STÁTY: {staty_string}"
        
    @property
    def staty_string(self):
        """Zobrazení seznamu státu jako string."""
        all_staty = self.stat.all()
        if all_staty:
            return ', '.join([stat.nazev for stat in all_staty])
        else:
            return 'Není přiřazen žádný stát.'
        
    @property
    def stoleti_string(self):
        """Zobrazení seznamu století jako string."""
        all_stoleti = self.stoleti.all()
        if all_stoleti:
            return ', '.join([stoleti.nazev for stoleti in all_stoleti])
        else:
            return 'Není přiřazeno žádné století.'
        
    def get_data(self):
        """Kompletní výpis informací o objektu."""
        data = f'SKUPINA BOJOVNIC: {self.jmeno}'
        data += f"\nNAPOJENÁ STOLETÍ: {self.stoleti_string}"
        data += f"\nNAPOJENÉ STÁTY: {self.staty_string}"
        data += "\nNAPOJENÉ BOJOVNICE:"
        if self.bojovnice.count() == 0:
            data += "\n- století není napojeno na žádné bojovnice"
        else:
            for each in self.bojovnice.all():
                data += f"- {each.admin_string}\n"
        data += f"\nPOPIS: {self.popis}"

        return data
        
    def get_absolute_url_detail(self):
        """Vrátí URL adresu detailu instance pro podaplikaci správy."""
        return reverse('sprava:skupiny-bojovnic-admin-detail', kwargs={'pk': self.pk})

    def get_absolute_url_update(self):
        """Vrátí URL adresu stránky, kde je možné instanci upravit. """
        return reverse('sprava:skupiny-bojovnic-admin-update', kwargs={'pk': self.pk})
    
    def get_absolute_url_delete(self):
        """Vrátí URL adresu stránky, kde je možné instanci instanci smazat z DTB. """
        return reverse('sprava:skupiny-bojovnic-admin-delete', kwargs={'pk': self.pk})
    
    def get_absolute_url_bojovnice_app(self):
        """Vrátí URL adresu detailu instance pro uživatelskou část aplikace."""
        return reverse('group_detail_bojovnice_app', kwargs={'pk': self.pk})
    
    def is_bojovnice(self):
        """Slouží k rozlišení modelů v template listing pro bojovnice APP """
        return False
    
    def get_num_for_sort_by_stoleti(self):
        """Vrátí číslo pro řazení skupin podle století."""
        if self.stoleti.first() == None:
            return 0
        elif self.stoleti.count() == 1:
            return self.stoleti.first().pk
        else:
            return (self.stoleti.first().pk) + 0.5
        



