# Generated by Django 3.1.4 on 2020-12-12 02:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comps', '0009_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='max_age',
            new_name='year_from',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='min_age',
            new_name='year_to',
        ),
    ]