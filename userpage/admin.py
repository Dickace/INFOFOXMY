from django.contrib import admin
from .models import InfoBlock, Profile, Bracelet

# Register your models here.
admin.site.register(Profile)
admin.site.register(InfoBlock)
admin.site.register(Bracelet)