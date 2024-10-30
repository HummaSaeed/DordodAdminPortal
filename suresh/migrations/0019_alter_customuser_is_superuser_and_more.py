# Generated by Django 5.0.6 on 2024-10-19 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0018_rename_personal_pic_personalinformation_profile_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='email',
            field=models.EmailField(default='default@example.com', max_length=254),
        ),
    ]
