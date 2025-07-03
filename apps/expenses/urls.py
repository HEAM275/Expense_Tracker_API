from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.expenses.views.views import *


router = DefaultRouter()
router.register(r"expenses", ExpenseViewSet, basename="expenses")


urlpatterns = [
    path("", include(router.urls)),
]
