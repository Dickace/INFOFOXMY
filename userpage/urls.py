from django.urls import path
from .views import *


urlpatterns = [
    path('', ViewProfile.as_view()),
    path('add/', CreateProfile.as_view()),
    path('delete/', ProfileDeleteView.as_view()),
    path('profile/<int:pk>', InfoBlockfFromProfileListView.as_view()),
    path('profile/<int:pk>/delete', InfoBlockDeleteView.as_view()),
    path('profile/<int:pk>/change', InfoBlockChangeView.as_view()),
    path('profile/<int:pk>/disconnect', DisconnectBracelet.as_view()),
    # path('profile/<int:pk>/<int:pl>', InfoBlockDetailView.as_view()),
    # path('profile/<int:pk>/count', InfoBlockListCountView.as_view()),
    path('bracelet/add', createhandler.as_view()),
    path('bracelet/delete/<int:pk>', deleteHandler.as_view()),
    path('bracelet/<int:pk>', AccountDefinition.as_view()),
    path('bracelet/registration/<int:pk>', JoinHandler.as_view()),
]
