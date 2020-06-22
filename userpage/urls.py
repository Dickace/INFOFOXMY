from django.urls import path
from .views import *


urlpatterns = [
    path('', ViewProfile.as_view()),
    path('add/', CreateProfile.as_view()),
    path('delete/', ProfileDeleteView.as_view()),
    path('profile/', InfoBlockListView.as_view()),
    path('profile/delete/<int:pk>', InfoBlockDeleteView.as_view()),
    path('profile/change/<int:pk>', InfoBlockChangeView.as_view()),
    path('profile/<int:pk>', InfoBlockDetailView.as_view()),
    path('profile/count', InfoBlockListCountView.as_view()),
    path('bracelet/add', createhandler.as_view()),
    path('bracelet/delete/<int:pk>', deleteHandler.as_view()),
    path('bracelet/<int:pk>', AccountDefinition.as_view()),
    path('bracelet/registration/<int:pk>', JoinHandler.as_view()),
]
