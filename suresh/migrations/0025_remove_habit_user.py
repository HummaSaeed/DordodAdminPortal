# Generated by Django 5.0.6 on 2024-10-27 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0024_alter_opportunity_swot_analysis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habit',
            name='user',
        ),
    ]
