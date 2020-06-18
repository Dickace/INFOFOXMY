from django.urls import path
from .views import *


urlpatterns = [
    path('add', createhandler.as_view()),
    path('delete/<int:pk>', deleteHandler.as_view()),
    path('<int:pk>', AccountDefinition.as_view()),
    path('registration/<int:pk>', JoinHandler.as_view()),
]