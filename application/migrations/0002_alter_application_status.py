# Generated by Django 5.0.4 on 2024-05-20 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('Applied', 'Applied'), ('Declined', 'Declined'), ('Pending', 'Pending'), ('Accepted', 'Accepted')], default='Applied', max_length=50),
        ),
    ]
