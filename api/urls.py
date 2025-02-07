from django.urls import path
from .views import stats, fund

urlpatterns = [
    path("stats/", stats, name="stats"),
    path("fund/", fund, name="fund"),
]
