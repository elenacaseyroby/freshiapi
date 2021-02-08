# Generated by Django 3.1.5 on 2021-02-03 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0002_auto_20210130_0656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='one_serving_display_qty',
        ),
        migrations.RemoveField(
            model_name='food',
            name='one_serving_display_unit',
        ),
        migrations.AddField(
            model_name='food',
            name='one_serving_description',
            field=models.CharField(max_length=40, null=True),
        ),
    ]