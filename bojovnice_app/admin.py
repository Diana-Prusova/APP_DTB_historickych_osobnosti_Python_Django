"""
Modul nastavuje zobrazení modelů v Django administračním rozhraní.
"""

from django.contrib import admin
from bojovnice_app import models

@admin.register(models.Staty)
class StatyAdmin(admin.ModelAdmin):
    list_display = ('id', 'nazev')
    pass


@admin.register(models.Stoleti)
class StoletiAdmin(admin.ModelAdmin):
    list_display = ('id', 'nazev')
    pass


@admin.register(models.Bojovnice)
class BojovniceAdmin(admin.ModelAdmin):
    list_display = ('id', 'jmeno', 'obdobi', 'uzemi', 'popis', 'get_pribeh_info', 'get_stat', 'get_stoleti')

    @admin.display(description='délka příběhu')
    def get_pribeh_info(self, obj):
        return f'{len(obj.pribeh)} znaků'
    
    @admin.display(description='napojené státy')
    def get_stat(self, obj):
        return ', '.join([each.nazev for each in obj.stat.all()])
    
    @admin.display(description='napojená století')
    def get_stoleti(self, obj):
        return ', '.join([each.nazev for each in obj.stoleti.all()])

    
@admin.register(models.VsechnaJmena)
class VsechnaJmenaAdmin(admin.ModelAdmin):
    list_display = ('id', 'jmeno', 'bojovnice', 'hlavni_jmeno')
    pass


@admin.register(models.SkupinyBojovnic)
class SkupinyBojovnicAdmin(admin.ModelAdmin):
    list_display = ('id', 'jmeno', 'get_popis_info', 'get_stat', 'get_stoleti', 'get_bojovnice')

    @admin.display(description='popisu')
    def get_popis_info(self, obj):
        if len(obj.popis) > 10:
            return 'ano'
        else:
            return 'ne'

    @admin.display(description='napojené státy')
    def get_stat(self, obj):
        if obj.stat.all():
            return ', '.join([each.nazev for each in obj.stat.all()])
        else:
            return 'žádný'
        
    @admin.display(description='napojená století')
    def get_stoleti(self, obj):
        if obj.stoleti.all():
            return ', '.join([each.nazev for each in obj.stoleti.all()])
        else:
            return 'žádné'
        
    @admin.display(description='přiřazené bojovnice')
    def get_bojovnice(self, obj):
        if obj.bojovnice.all():
            return ', '.join([each.jmeno for each in obj.bojovnice.all()])
        else:
            return 'žádné'