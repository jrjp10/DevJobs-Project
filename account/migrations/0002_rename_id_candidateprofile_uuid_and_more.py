# Generated by Django 5.0.4 on 2024-04-09 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidateprofile',
            old_name='id',
            new_name='uuid',
        ),
        migrations.RenameField(
            model_name='companyprofile',
            old_name='id',
            new_name='uuid',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='id',
            new_name='uuid',
        ),
    ]
