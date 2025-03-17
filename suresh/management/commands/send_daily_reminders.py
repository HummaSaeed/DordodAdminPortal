from django.core.management.base import BaseCommand
from django.utils import timezone
from suresh.models import UserSettings, Habit
from suresh.utils import send_notification_email

class Command(BaseCommand):
    help = 'Send daily reminder emails to users'

    def handle(self, *args, **options):
        current_time = timezone.now().time()
        today = timezone.now().date()
        
        # Get all users who have email notifications enabled
        settings = UserSettings.objects.filter(
            email_notifications=True,
            reminder_time__hour=current_time.hour,
            reminder_time__minute=current_time.minute,
        ).select_related('user')

        for setting in settings:
            # Check if reminder already sent today
            if setting.last_reminder_sent == today:
                continue

            # Get active habits for the user
            habits = Habit.objects.filter(
                user=setting.user,
                is_active=True
            )

            if habits.exists():
                # Send email
                sent = send_notification_email(
                    user=setting.user,
                    subject="Daily Habit Reminder",
                    template='emails/reminder.html',
                    context={'habits': habits}
                )

                if sent:
                    setting.last_reminder_sent = today
                    setting.save()

        self.stdout.write(self.style.SUCCESS('Successfully sent reminder emails')) 