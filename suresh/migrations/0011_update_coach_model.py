from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0010_associate_coaches_with_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coach',
            name='availability',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='coach',
            name='certifications',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='coach',
            name='specializations',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='coach',
            name='social_media',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='coach',
            name='languages_spoken',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ] 