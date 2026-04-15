from django.urls import path
from api.views import HomeView, ExerciseView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('workout/', ExerciseView.as_view(), name='workout'),
]