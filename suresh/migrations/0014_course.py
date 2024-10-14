# Generated by Django 5.0.6 on 2024-09-22 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0013_maingoal_subgoal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=100, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('details', models.TextField()),
                ('instructor', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('credit_hours', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]