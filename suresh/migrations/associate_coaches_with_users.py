from django.db import migrations

def associate_coaches_with_users(apps, schema_editor):
    Coach = apps.get_model('suresh', 'Coach')
    CustomUser = apps.get_model('suresh', 'CustomUser')
    
    # For each coach without a user, try to find a matching user by email
    for coach in Coach.objects.filter(user__isnull=True):
        try:
            user = CustomUser.objects.get(email=coach.email)
            coach.user = user
            coach.save()
        except CustomUser.DoesNotExist:
            # If no matching user is found, leave the coach as is
            pass

def reverse_associate_coaches(apps, schema_editor):
    # No need to reverse this migration
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0008_alter_coach_email_moodtracking'),
    ]

    operations = [
        migrations.RunPython(associate_coaches_with_users, reverse_associate_coaches),
    ] 