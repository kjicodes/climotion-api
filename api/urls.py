from django.urls import path
from api.views import HomeView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
]