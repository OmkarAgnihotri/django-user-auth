from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import SimpleRouter
from .views import UserAuthViewSet

router = SimpleRouter(trailing_slash=False)

router.register('auth',UserAuthViewSet,basename='auth')

urlpatterns = router.urls
