# Generated by Django 3.1.5 on 2021-02-07 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0003_auto_20210203_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodusdafood',
            name='food',
            field=models.ForeignKey(db_column='food_id', on_delete=django.db.models.deletion.CASCADE, to='foods.food'),
        ),
    ]