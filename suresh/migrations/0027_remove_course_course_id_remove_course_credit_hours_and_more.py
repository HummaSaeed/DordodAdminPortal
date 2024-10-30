# Generated by Django 5.0.6 on 2024-10-29 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0026_habit_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_id',
        ),
        migrations.RemoveField(
            model_name='course',
            name='credit_hours',
        ),
        migrations.RemoveField(
            model_name='course',
            name='details',
        ),
        migrations.RemoveField(
            model_name='course',
            name='instructor',
        ),
        migrations.AddField(
            model_name='course',
            name='discount_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='discount_percentage',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='discount_start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]