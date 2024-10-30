# Generated by Django 5.0.6 on 2024-10-19 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0017_habit_created_at_habit_is_active_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personalinformation',
            old_name='personal_pic',
            new_name='profile_picture',
        ),
        migrations.AddField(
            model_name='personalinformation',
            name='email',
            field=models.EmailField(default='default@example.com', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='personalinformation',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='personalinformation',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='birth_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='city',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='country',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='date_of_birth',
            field=models.DateField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='marital_status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='nationality',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='preferred_full_name',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='state',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
