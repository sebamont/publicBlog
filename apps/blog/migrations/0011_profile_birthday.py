# Generated by Django 3.0.4 on 2020-04-18 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20200418_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name="author's B-day"),
        ),
    ]
