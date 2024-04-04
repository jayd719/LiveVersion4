# Generated by Django 5.0.1 on 2024-04-04 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worderTracker', '0005_machines'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompltedOrders',
            fields=[
                ('jobNumber', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('customer', models.CharField(max_length=50)),
                ('des', models.TextField()),
                ('qty', models.CharField(max_length=5)),
                ('dueDate', models.DateField()),
                ('TA', models.CharField(max_length=5)),
                ('estimatedHours', models.FloatField()),
                ('actualHours', models.FloatField()),
                ('completedDate', models.DateField(auto_now_add=True, verbose_name='Date')),
            ],
        ),
    ]
