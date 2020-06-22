from django.db import models
from myauth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_activated = models.BooleanField(default=False)

    def __int__(self):
        return self.id

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиля'


class InfoBlock(models.Model):
    title = models.CharField(max_length=65, verbose_name='Название')
    content = models.TextField(max_length=650, verbose_name='Содержание')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Инфоблок'
        verbose_name_plural = 'Инфоблоки'


class bracelet(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    unique_code = models.CharField(max_length=6, unique=True)
    is_activated = models.BooleanField()

    def __int__(self):
        return self.id

    class Meta:
        verbose_name = 'Носитель'
        verbose_name_plural = 'Носители'
