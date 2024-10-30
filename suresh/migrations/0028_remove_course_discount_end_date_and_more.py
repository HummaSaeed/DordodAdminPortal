# Generated by Django 5.0.6 on 2024-10-29 14:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0027_remove_course_course_id_remove_course_credit_hours_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='discount_end_date',
        ),
        migrations.RemoveField(
            model_name='course',
            name='discount_percentage',
        ),
        migrations.RemoveField(
            model_name='course',
            name='discount_start_date',
        ),
        migrations.AddField(
            model_name='course',
            name='credit_hours',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='course',
            name='purchasers',
            field=models.ManyToManyField(related_name='purchased_courses', to=settings.AUTH_USER_MODEL),
        ),
    ]