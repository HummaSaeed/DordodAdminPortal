# Generated by Django 5.0.6 on 2024-12-10 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0030_remove_course_discount_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='discount_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='discount_percentage',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='discount_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
