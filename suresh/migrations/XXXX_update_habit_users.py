from django.db import migrations
from django.conf import settings

def set_default_user(apps, schema_editor):
    Habit = apps.get_model('suresh', 'Habit')
    User = apps.get_model(settings.AUTH_USER_MODEL.split('.')[0], settings.AUTH_USER_MODEL.split('.')[1])
    
    # Get the first superuser or create one if none exists
    default_user = User.objects.filter(is_superuser=True).first()
    
    if not default_user:
        # If no superuser exists, get the first user
        default_user = User.objects.first()
    
    if default_user:
        # Update all habits that have no user
        Habit.objects.filter(user__isnull=True).update(user=default_user)

def reverse_default_user(apps, schema_editor):
    # No need to reverse this operation
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0017_habit_created_at_habit_is_active_and_more'),  # Updated to use the correct migration
    ]

    operations = [
        migrations.RunPython(set_default_user, reverse_default_user),
    ] 