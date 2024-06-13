from django.contrib import admin
from django.urls import path, include

from bojovnice_app import views

urlpatterns = [
    # ADMIN DJANGO ROZHRANÍ
    path('admin/', admin.site.urls),
    # API
    path('api/', include('bojovnice_api.urls'), name='bojovnice_api'),
    # SPRÁVA APLIKACE
    path('sprava/', include('sprava.urls')),
    # BOJOVNICE APP PRO UŽIVATELE
    path('', views.BojovniceAppIndexView.as_view(), name='index_bojovnice_app'),
    path('bojovnice/', views.BojovniceAppListBojovniceView.as_view(), name='listing_bojovnice_app'),
    path('bojovnice/<int:pk>/', views.BojovniceAppDetailBojovniceView.as_view(), name='one_detail_bojovnice_app'),
    path('skupiny/', views.BojovniceAppListSkupinyBojovnicView.as_view(), name='listing_skupiny_app'),
    path('skupiny/<int:pk>/', views.BojovniceAppDetailSkupinyBojovnicView.as_view(), name='group_detail_bojovnice_app'),
]
