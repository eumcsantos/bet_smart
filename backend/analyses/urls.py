from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatchViewSet

# O Router do DRF cria automaticamente as rotas /matches/ (GET/POST)
router = DefaultRouter()
router.register(r'matches', MatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]