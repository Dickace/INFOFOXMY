# Generated by Django 3.0.7 on 2020-06-23 14:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('is_activated', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='InfoBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=65, verbose_name='Название')),
                ('content', models.TextField(max_length=650, verbose_name='Содержание')),
                ('profile', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='userpage.Profile')),
            ],
            options={
                'verbose_name': 'Инфоблок',
                'verbose_name_plural': 'Инфоблоки',
            },
        ),
        migrations.CreateModel(
            name='Bracelet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_code', models.CharField(max_length=8, unique=True, validators=[django.core.validators.MinLengthValidator(8)])),
                ('profile', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bracelets', to='userpage.Profile')),
            ],
            options={
                'verbose_name': 'Носитель',
                'verbose_name_plural': 'Носители',
            },
        ),
    ]
