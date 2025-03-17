from django.db import models
import json
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)



# Custom user model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# Personal Information Model
class PersonalInformation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # New field
    first_name = models.CharField(max_length=30,blank=True,null=True)
    middle_name = models.CharField(max_length=30, blank=True,null=True)
    last_name = models.CharField(max_length=30,blank=True,null=True)
    preferred_full_name = models.CharField(max_length=60, blank=True,null=True)
    email = models.EmailField(default='default@example.com')
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    nationality = models.CharField(max_length=30,blank=True,null=True)
    date_of_birth = models.DateField(max_length=30,blank=True,null=True)
    birth_name = models.CharField(max_length=30, blank=True,null=True)
    marital_status = models.CharField(max_length=20,blank=True,null=True)
    suffix = models.CharField(max_length=10, blank=True,null=True)
    gender = models.CharField(max_length=10,blank=True,null=True)
    country = models.CharField(max_length=30,blank=True,null=True)
    state = models.CharField(max_length=30,blank=True,null=True)
    city = models.CharField(max_length=30,blank=True,null=True)

    def __str__(self):
     return self.first_name if self.first_name else "Unnamed Person"

# Global Information Model
class GlobalInformation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nationality = models.CharField(max_length=100, default="Not Specified")
    current_location = models.CharField(max_length=200, default="Not Specified")
    languages = models.JSONField(default=list, blank=True)
    time_zone = models.CharField(max_length=50, default="UTC")
    availability = models.CharField(max_length=200, default="Full-time")
    preferred_communication = models.CharField(max_length=100, default="Email")
    social_media_links = models.JSONField(default=dict, blank=True)
    hobbies_interests = models.TextField(default="Not specified")
    volunteer_work = models.TextField(default="None")
    travel_experience = models.TextField(default="None")
    cultural_background = models.TextField(default="Not specified")
    dietary_preferences = models.CharField(max_length=200, default="None")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Global Information"

    def save(self, *args, **kwargs):
        if self.languages is None:
            self.languages = []
        if self.social_media_links is None:
            self.social_media_links = {}
        super().save(*args, **kwargs)

# Professional Information Model
class ProfessionalInformation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    work_experiences = models.ManyToManyField('WorkExperience', blank=True, related_name='professional_informations')
    previous_experiences = models.ManyToManyField('PreviousExperience', blank=True)
    educations = models.ManyToManyField('Education', blank=True)
    language_skills = models.ManyToManyField('LanguageSkill', blank=True)
    certificates = models.ManyToManyField('Certificate', blank=True)
    honors_awards_publications = models.ManyToManyField('HonorsAwardsPublications', blank=True, related_name='professional_informations')
    functional_skills = models.ManyToManyField('FunctionalSkill', blank=True)
    technical_skills = models.ManyToManyField('TechnicalSkill', blank=True)

    def __str__(self):
        return f"{self.user.first_name}'s Professional Info"
# Work Experience Model
class WorkExperience(models.Model):
    professional_info = models.ForeignKey(ProfessionalInformation, related_name='work_experiences_set', on_delete=models.CASCADE, blank=True, null=True)
    organization_name = models.CharField(max_length=100, blank=True, null=True)
    organization_location = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    is_current = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.organization_name} ({self.start_date} - {self.end_date})"

# Previous Experience Model
class PreviousExperience(models.Model):
    professional_info = models.ForeignKey(ProfessionalInformation, on_delete=models.CASCADE, related_name='previous_experience', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    job_responsibilities = models.TextField()

    def __str__(self):
        return f"{self.title} at {self.company_name}"

# Education Model
class Education(models.Model):
    professional_info = models.ForeignKey(ProfessionalInformation, on_delete=models.CASCADE, related_name='educations_set', blank=True, null=True)
    college_university = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    area_of_study = models.CharField(max_length=100)
    degree_completed = models.BooleanField(default=False)
    date_completed = models.DateField()

    def __str__(self):
        return f"{self.degree} from {self.college_university}"

# Language Skill Model
class LanguageSkill(models.Model):
    professional_info = models.ForeignKey(ProfessionalInformation, on_delete=models.CASCADE, related_name='language_skills_set', blank=True, null=True)
    language = models.CharField(max_length=50)
    speaking_proficiency = models.CharField(max_length=50)
    writing_proficiency = models.CharField(max_length=50)
    reading_proficiency = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.language} - Speaking: {self.speaking_proficiency}"

# Certificate Model
class Certificate(models.Model):
    professional_info = models.ForeignKey(ProfessionalInformation, on_delete=models.CASCADE, related_name='certificates_set', blank=True, null=True)
    certification_license = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    institution = models.CharField(max_length=100)
    effective_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    attachment = models.FileField(upload_to='certificates/', blank=True, null=True)

    def __str__(self):
        return f"{self.certification_license} from {self.institution}"

# Honors, Awards, and Publications Model
class HonorsAwardsPublications(models.Model):
    professional_info = models.ForeignKey(ProfessionalInformation, on_delete=models.CASCADE, related_name='honors_awards_set', blank=True, null=True)
    honor_reward_publication = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    institution = models.CharField(max_length=100)
    issue_date = models.DateField()
    attachment = models.FileField(upload_to='honors/', blank=True, null=True)

    def __str__(self):
        return f"{self.honor_reward_publication} - {self.issue_date}"

# Functional Skill Model
class FunctionalSkill(models.Model):
    professional_info = models.ForeignKey(ProfessionalInformation, on_delete=models.CASCADE, related_name='functional_skills_set', blank=True, null=True)
    skill = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.skill} - Proficiency: {self.proficiency}"

# Technical Skill Model
class TechnicalSkill(models.Model):
    professional_info = models.ForeignKey(ProfessionalInformation, on_delete=models.CASCADE, related_name='technical_skills_set', blank=True, null=True)
    skill = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.skill} - Proficiency: {self.proficiency}"

class DocumentUpload(models.Model):
    DOCUMENT_TYPES = (
        ('resume', 'Resume'),
        ('cover_letter', 'Cover Letter'),
        ('portfolio', 'Portfolio'),
        ('education', 'Educational Document'),
        ('professional', 'Professional Document'),
        ('bank', 'Bank Document'),
        ('other', 'Other Document'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document_type = models.CharField(choices=DOCUMENT_TYPES, max_length=20)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.document_type}"
class WorkItem(models.Model):
    WORK_TYPES = (
        ('post', 'Post'),
        ('article', 'Article'),
        ('video', 'Video'),
        ('journal', 'Journal'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='work_items')
    work_type = models.CharField(choices=WORK_TYPES, max_length=10)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.work_type}) - {self.user.email}"
class SwotAnalysis(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='swot_analyses')

    def __str__(self):
        return f"SWOT Analysis for {self.user.email}"

    def save(self, *args, **kwargs):
        creating = not self.pk  # Check if this is a new instance
        super().save(*args, **kwargs)
        if creating:
            # Create default entries for SWOT components
            Strength.objects.create(swot_analysis=self, description="Default Strength")
            Weakness.objects.create(swot_analysis=self, description="Default Weakness")
            Opportunity.objects.create(swot_analysis=self, description="Default Opportunity")
            Threat.objects.create(swot_analysis=self, description="Default Threat")

class Strength(models.Model):
    swot_analysis = models.ForeignKey(SwotAnalysis, on_delete=models.CASCADE, related_name='strengths')
    description = models.TextField()

    def __str__(self):
        return self.description

class Weakness(models.Model):
    swot_analysis = models.ForeignKey(SwotAnalysis, on_delete=models.CASCADE, related_name='weaknesses')
    description = models.TextField()

    def __str__(self):
        return self.description

class Opportunity(models.Model):
    swot_analysis = models.ForeignKey(
        SwotAnalysis, 
        on_delete=models.CASCADE, 
        related_name='opportunities',
        null=True,  # Keep this nullable for existing records
        default=None  # Add a default value
    )
    description = models.TextField()

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        # If no swot_analysis is set, create a new one for the user
        if not self.swot_analysis:
            # You might need to adjust this to get the correct user
            user = self.swot_analysis.user if self.swot_analysis else None
            if user:
                self.swot_analysis, _ = SwotAnalysis.objects.get_or_create(user=user)
        super().save(*args, **kwargs)

class Threat(models.Model):
    swot_analysis = models.ForeignKey(SwotAnalysis, on_delete=models.CASCADE, related_name='threats')
    description = models.TextField()

    def __str__(self):
        return self.description

class MainGoal(models.Model):
    GOAL_CATEGORIES = [
        ('spiritual', 'Spiritual Goals'),
        ('fitness', 'Fitness Goals'),
        ('family', 'Family Goals'),
        ('career', 'Career Goals'),
        ('financial', 'Financial Goals'),
        ('social', 'Social Goals'),
        ('intellectual', 'Intellectual Goals')
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=GOAL_CATEGORIES)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)
    weightage = models.FloatField(default=1.0)

    def __str__(self):
        return self.name

# SubGoal Model
class SubGoal(models.Model):
    main_goal = models.ForeignKey(MainGoal, related_name='subgoals', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)
    required_effort = models.FloatField(default=0)
    spent_effort = models.FloatField(default=0)
    coach = models.CharField(max_length=255, blank=True, null=True)
    accomplishment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} (SubGoal of {self.main_goal.name})"
class Course(models.Model):
    title = models.CharField(max_length=255)
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="courses"
    )
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    credit_hours = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    purchasers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='purchased_courses')

    def __str__(self):
        return self.title

    @property
    def final_price(self):
        return self.discounted_price if self.discounted_price else self.price

class VideoLecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_lectures")
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to="course_videos/")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    video_lecture = models.ForeignKey(VideoLecture, on_delete=models.CASCADE, related_name="quizzes")
    question = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])

    def __str__(self):
        return self.question

class Habit(models.Model):
    CATEGORIES = [
        ('health', 'Health & Fitness'),
        ('learning', 'Learning & Growth'),
        ('productivity', 'Productivity'),
        ('mindfulness', 'Mindfulness'),
        ('social', 'Social & Family'),
        ('career', 'Career'),
    ]

    FREQUENCIES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    PRIORITIES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    frequency = models.CharField(max_length=20, choices=FREQUENCIES, default='daily')
    priority = models.CharField(max_length=20, choices=PRIORITIES, default='medium')
    description = models.TextField(blank=True)
    target_value = models.IntegerField(default=1)
    unit = models.CharField(max_length=50, blank=True)
    reminder_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    streak = models.IntegerField(default=0)
    last_completed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.email}"

# Add this to your existing models.py
class UserSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='settings')
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    reminder_time = models.TimeField(default='09:00')
    dark_mode = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "User Settings"

    def __str__(self):
        return f"{self.user.email}'s Settings"
