# Generated by Django 5.0.7 on 2024-07-24 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employeemonthlydata'),
        ('site_base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workschedule',
            name='name_of_employees',
        ),
        migrations.AddField(
            model_name='workschedule',
            name='employees',
            field=models.ManyToManyField(blank=True, related_name='shifts', to='employee.employee'),
        ),
        migrations.AlterField(
            model_name='workschedule',
            name='num_of_employees',
            field=models.PositiveIntegerField(),
        ),
    ]
