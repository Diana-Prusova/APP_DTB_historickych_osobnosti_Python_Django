from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bojovnice_api import views

router = DefaultRouter()
router.register('bojovnice', views.BojovniceViewSet)
router.register('skupiny-bojovnic', views.SkupinyBojovnicViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

app_name = 'bojovnice_api'