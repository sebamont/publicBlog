# Generated by Django 3.0.4 on 2020-04-08 19:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200408_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.AddField(
            model_name='profile',
            name='alias',
            field=models.CharField(default=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL), max_length=100, verbose_name='author Alias'),
        ),
    ]
