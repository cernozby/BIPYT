# Generated by Django 3.1.4 on 2020-12-12 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comps', '0010_auto_20201212_0314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='comp_id',
        ),
    ]
