# Generated by Django 3.1.5 on 2021-07-14 17:07

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_email', models.EmailField(max_length=254, verbose_name='From email')),
                ('to_emails', django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(blank=True, max_length=254, verbose_name='To email'), size=None)),
                ('subject', models.CharField(blank=True, max_length=255, null=True)),
                ('msg', models.TextField(blank=True, null=True)),
                ('html_msg', models.TextField(blank=True, null=True)),
                ('sent_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('error', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'communications_emails',
            },
        ),
    ]
