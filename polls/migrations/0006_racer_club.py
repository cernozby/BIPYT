# Generated by Django 3.1.4 on 2020-12-22 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_racer_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='racer',
            name='club',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]