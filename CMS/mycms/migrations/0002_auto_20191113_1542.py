# Generated by Django 2.1.2 on 2019-11-13 07:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mycms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cms',
            name='create_time',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='cms',
            name='update_time',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
