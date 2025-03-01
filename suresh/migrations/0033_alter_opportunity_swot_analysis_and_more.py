# Generated by Django 5.0.6 on 2024-12-11 14:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0032_remove_course_discount_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunity',
            name='swot_analysis',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opportunities', to='suresh.swotanalysis'),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
