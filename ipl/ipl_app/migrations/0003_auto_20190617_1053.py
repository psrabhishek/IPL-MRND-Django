# Generated by Django 2.2.1 on 2019-06-17 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipl_app', '0002_auto_20190617_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='umpire1',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
