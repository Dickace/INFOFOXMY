from django.db import models


class codeHandler(models.Model):
    profile_id = models.IntegerField(blank=True, null=True, max_length=24)
    unique_code = models.CharField(max_length=6, unique=True)
    is_activated = models.BooleanField()

    def __int__(self):
        return self.id

    class Meta:
        verbose_name = 'Носитель'
        verbose_name_plural = 'Носители'

