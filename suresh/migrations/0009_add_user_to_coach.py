from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0008_alter_coach_email_moodtracking'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='suresh.customuser'),
        ),
    ] 