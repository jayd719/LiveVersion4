# Generated by Django 5.0.1 on 2024-04-04 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worderTracker', '0008_alter_workordertracker_des'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
