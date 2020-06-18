from django.urls import path, include
from. views import *

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('is_admin', is_admin),

]
