from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0011_update_coach_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accomplishment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('professional', 'Professional'), ('academic', 'Academic'), ('personal', 'Personal'), ('certification', 'Certification'), ('award', 'Award'), ('project', 'Project'), ('publication', 'Publication'), ('volunteer', 'Volunteer')], default='professional', max_length=20)),
                ('date', models.DateField()),
                ('impact', models.TextField(blank=True, null=True)),
                ('evidence', models.FileField(blank=True, null=True, upload_to='accomplishments/')),
                ('is_public', models.BooleanField(default=False)),
                ('tags', models.JSONField(blank=True, default=list)),
                ('skills_used', models.JSONField(blank=True, default=list)),
                ('metrics', models.JSONField(blank=True, default=dict)),
                ('external_links', models.JSONField(blank=True, default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suresh.customuser')),
            ],
            options={
                'verbose_name': 'Accomplishment',
                'verbose_name_plural': 'Accomplishments',
                'ordering': ['-date', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AccomplishmentShare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('linkedin', 'LinkedIn'), ('twitter', 'Twitter'), ('facebook', 'Facebook'), ('email', 'Email'), ('connections', 'Connections'), ('portfolio', 'Portfolio')], max_length=20)),
                ('shared_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField(blank=True)),
                ('is_successful', models.BooleanField(default=True)),
                ('accomplishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suresh.accomplishment')),
            ],
            options={
                'ordering': ['-shared_at'],
            },
        ),
    ] 