"""
Vytvořeny serializátory pro modely Bojovnice a SkupinyBojovnic.
Jsou upravené tak, aby vracely názvy spojených entit, nikoliv jejich ID.
"""
from rest_framework import serializers
from bojovnice_app import models


class BojovniceSerializer(serializers.ModelSerializer):
    """ 
    Serializátor pro model Bojovnice.
    """
    stat = serializers.SerializerMethodField()
    vsechna_jmena = serializers.SerializerMethodField()

    class Meta:
        model = models.Bojovnice
        fields = [
            'id', 
            'jmeno', 
            'obdobi', 
            'uzemi',
            'stat', 
            'vsechna_jmena',
            'popis', 
            'pribeh'
        ]

    def get_stat(self, obj):
        return [each.nazev for each in obj.stat.all()]

    def get_stoleti(self, obj):
        return [each.nazev for each in obj.stoleti.all()]

    def get_vsechna_jmena(self, obj):
        return [each.jmeno for each in obj.vsechnajmena_set.all()]


class SkupinyBojovnicSerializer(serializers.ModelSerializer):
    """ 
    Serializátor pro model Skupiny Bojovnic.
    """
    stat = serializers.SerializerMethodField()
    stoleti = serializers.SerializerMethodField()
    bojovnice = serializers.SerializerMethodField()

    class Meta:
        model = models.SkupinyBojovnic
        fields = [
            'jmeno',
            'stat',
            'stoleti',
            'bojovnice',
            'popis'
        ]

    def get_stat(self, obj):
        return [each.nazev for each in obj.stat.all()]
    
    def get_stoleti(self, obj):
        return [each.nazev for each in obj.stoleti.all()]
    
    def get_bojovnice(self, obj):
        return [each.jmeno for each in obj.bojovnice.all()]


