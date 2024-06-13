from django.urls import path
from sprava import views

app_name = 'sprava'

urlpatterns = [
    # INDEX
    path('', views.IndexSpravaView.as_view(), name='index-sprava'),
    # DOWLAND DATA
    path('download-data', views.DownloadDataView.as_view(), name='download-data'),
    # LOGIN
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # STÁTY
    path('staty/', views.StatyAdminListView.as_view(), name='staty-admin-list'),
    path('staty/<int:pk>/', views.StatyAdminDetailView.as_view(), name='staty-admin-detail'),
    path('staty/vytvorit/', views.StatyAdminCreateView.as_view(), name='staty-admin-create'),
    path('staty/upravit/<int:pk>/', views.StatyAdminUpdateView.as_view(), name='staty-admin-update'),
    path('staty/smazat/<int:pk>/', views.StatyAdminDeleteView.as_view(), name='staty-admin-delete'),
    # STOLETÍ
    path('stoleti/', views.StoletiAdminListView.as_view(), name='stoleti-admin-list'),
    path('stoleti/<int:pk>/', views.StoletiAdminDetailView.as_view(), name='stoleti-admin-detail'),
    path('stoleti/vytvorit/', views.StoletiAdminCreateView.as_view(), name='stoleti-admin-create'),
    path('stoleti/upravit/<int:pk>/', views.StoletiAdminUpdateView.as_view(), name='stoleti-admin-update'),
    path('stoleti/smazat/<int:pk>/', views.StoletiAdminDeleteView.as_view(), name='stoleti-admin-delete'),
    # BOJOVNICE
    path('bojovnice/', views.BojovniceAdminListView.as_view(), name='bojovnice-admin-list'),
    path('bojovnice/<int:pk>/', views.BojovniceAdminDetailView.as_view(), name='bojovnice-admin-detail'),
    path('bojovnice/vytvorit/', views.BojovniceAdminCreateView.as_view(), name='bojovnice-admin-create'),
    path('bojovnice/upravit/<int:pk>/', views.BojovniceAdminUpdateView.as_view(), name='bojovnice-admin-update'),
    path('bojovnice/smazat/<int:pk>/', views.BojovniceAdminDeleteView.as_view(), name='bojovnice-admin-delete'),
    # VŠECHNA JMÉNA
    path('vsechna-jmena/', views.VsechnaJmenaAdminListView.as_view(), name='vsechna-jmena-admin-list'),
    path('vsechna-jmena/<int:pk>/', views.VsechnaJmenaAdminDetailView.as_view(), name='vsechna-jmena-admin-detail'),
    path('vsechna-jmena/vytvorit/', views.VsechnaJmenaAdminCreateView.as_view(), name='vsechna-jmena-admin-create'),
    path('vsechna-jmena/upravit/<int:pk>/', views.VsechnaJmenaAdminUpdateView.as_view(), name='vsechna-jmena-admin-update'),
    path('vsechna-jmena/smazat/<int:pk>/', views.VsechnaJmenaAdminDeleteView.as_view(), name='vsechna-jmena-admin-delete'),
    # SKUPINY BOJOVNIC
    path('skupiny-bojovnic/', views.SkupinyBojovnicAdminListView.as_view(), name='skupiny-bojovnic-admin-list'),
    path('skupiny-bojovnic/<int:pk>/', views.SkupinyBojovnicAdminDetailView.as_view(), name='skupiny-bojovnic-admin-detail'),
    path('skupiny-bojovnic/vytvorit/', views.SkupinyBojovnicAdminCreateView.as_view(), name='skupiny-bojovnic-admin-create'),
    path('skupiny-bojovnic/upravit/<int:pk>/', views.SkupinyBojovnicAdminUpdateView.as_view(), name='skupiny-bojovnic-admin-update'),
    path('skupiny-bojovnic/smazat/<int:pk>/', views.SkupinyBojovnicAdminDeleteView.as_view(), name='skupiny-bojovnic-admin-delete'),
]