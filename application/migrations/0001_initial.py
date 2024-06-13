# Generated by Django 5.0.4 on 2024-05-17 13:34

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0005_alter_candidateprofile_candidate_image_and_more'),
        ('job', '0002_rename_address_job_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('application_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('applied', 'Applied'), ('reviewed', 'Reviewed'), ('interviewed', 'Interviewed'), ('rejected', 'Rejected'), ('hired', 'Hired')], default='applied', max_length=50)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='account.candidateprofile')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='job.job')),
            ],
        ),
    ]
