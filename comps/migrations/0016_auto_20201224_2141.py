# Generated by Django 3.1.4 on 2020-12-24 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comps', '0015_auto_20201223_1855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='lead_route_3',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='lead_route_4',
        ),
        migrations.AddField(
            model_name='registration',
            name='final',
            field=models.CharField(default=0, max_length=4),
        ),
    ]
