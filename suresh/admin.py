from django.contrib import admin
from django.utils.safestring import mark_safe
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    CustomUser, PersonalInformation, GlobalInformation, PreviousExperience, Course,
    ProfessionalInformation, TechnicalSkill, WorkExperience, Education, Habit,
    LanguageSkill, Certificate, HonorsAwardsPublications, FunctionalSkill, DocumentUpload,
    WorkItem, SwotAnalysis, MainGoal, SubGoal,Strength,Weakness,Opportunity,Threat,Quiz,VideoLecture
)

# Define a custom admin class for CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser',
        'middle_name', 'preferred_full_name', 'phone_number', 'nationality',
        'marital_status', 'suffix', 'date_of_birth', 'birth_name', 'gender', 
        'country', 'state', 'city'
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('personalinformation')
    def jwt_token(self, obj):
        # Generate token for the user
     token = RefreshToken.for_user(obj)
     return mark_safe(f'<span>{token.access_token}</span>')  # Displaying the token
    jwt_token.short_description = 'JWT Token'
    jwt_token.allow_tags = True 

    def middle_name(self, obj):
        return obj.personalinformation.middle_name if obj.personalinformation and obj.personalinformation.middle_name else 'N/A'
    middle_name.short_description = 'Middle Name'

    def preferred_full_name(self, obj):
        return obj.personalinformation.preferred_full_name if obj.personalinformation and obj.personalinformation.preferred_full_name else 'N/A'
    preferred_full_name.short_description = 'Preferred Full Name'

    def phone_number(self, obj):
        return obj.personalinformation.phone_number if obj.personalinformation and obj.personalinformation.phone_number else 'N/A'
    phone_number.short_description = 'Phone Number'

    def nationality(self, obj):
        return obj.personalinformation.nationality if obj.personalinformation and obj.personalinformation.nationality else 'N/A'
    nationality.short_description = 'Nationality'

    def marital_status(self, obj):
        return obj.personalinformation.marital_status if obj.personalinformation and obj.personalinformation.marital_status else 'N/A'
    marital_status.short_description = 'Marital Status'

    def suffix(self, obj):
        return obj.personalinformation.suffix if obj.personalinformation and obj.personalinformation.suffix else 'N/A'
    suffix.short_description = 'Suffix'

    def date_of_birth(self, obj):
        return obj.personalinformation.date_of_birth if obj.personalinformation and obj.personalinformation.date_of_birth else 'N/A'
    date_of_birth.short_description = 'Date of Birth'

    def birth_name(self, obj):
        return obj.personalinformation.birth_name if obj.personalinformation and obj.personalinformation.birth_name else 'N/A'
    birth_name.short_description = 'Birth Name'

    def gender(self, obj):
        return obj.personalinformation.gender if obj.personalinformation and obj.personalinformation.gender else 'N/A'
    gender.short_description = 'Gender'

    def country(self, obj):
        return obj.personalinformation.country if obj.personalinformation and obj.personalinformation.country else 'N/A'
    country.short_description = 'Country'

    def state(self, obj):
        return obj.personalinformation.state if obj.personalinformation and obj.personalinformation.state else 'N/A'
    state.short_description = 'State'

    def city(self, obj):
        return obj.personalinformation.city if obj.personalinformation and obj.personalinformation.city else 'N/A'
    city.short_description = 'City'


class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 1  # Number of empty forms to display


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1  # Number of empty forms to display


class LanguageSkillInline(admin.TabularInline):
    model = LanguageSkill
    extra = 1  # Number of empty forms to display


class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 1  # Number of empty forms to display


class HonorsAwardsInline(admin.TabularInline):
    model = HonorsAwardsPublications
    extra = 1


class FunctionalSkillInline(admin.TabularInline):
    model = FunctionalSkill
    extra = 1  # Number of empty forms to display


class PersonalInformationAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'display_profile_picture', 'middle_name', 'preferred_full_name',
        'phone_number', 'nationality', 'marital_status', 'suffix',
        'date_of_birth', 'birth_name', 'gender', 'country', 'state', 'city'
    )
    search_fields = ('user__email', 'preferred_full_name')
    ordering = ('user',)

    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" style="width: 50px; height: auto;" />')
        return 'No Image'  # Fallback if no image exists
    display_profile_picture.short_description = 'Profile Picture'


class GlobalInformationAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'date_learned', 'challenge_group', 'degree_of_challenge',
        'type_of_challenge', 'issuing_authority', 'reference_number',
        'religion', 'number_of_children', 'occupational_code', 'father_husband_guardian_name'
    )
    search_fields = ('user__email', 'challenge_group')
    ordering = ('user',)


class TechnicalSkillAdmin(admin.ModelAdmin):
    list_display = ('skill', 'proficiency')
    search_fields = ('skill',)
    ordering = ('skill',)


class ProfessionalInformationAdmin(admin.ModelAdmin):
    inlines = [WorkExperienceInline, EducationInline, LanguageSkillInline, CertificateInline, HonorsAwardsInline, FunctionalSkillInline]
    list_display = ('user', 'get_work_experiences')
    search_fields = ('user__email',)
    ordering = ('user',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('work_experiences', 'educations', 'language_skills', 'certificates', )

    def get_work_experiences(self, obj):
        return ', '.join(experience.organization_name for experience in obj.work_experiences.all()) if obj.work_experiences.exists() else 'No experience'
    get_work_experiences.short_description = 'Work Experiences'


class EducationAdmin(admin.ModelAdmin):
    list_display = ('college_university', 'degree', 'area_of_study', 'degree_completed', 'date_completed')
    search_fields = ('college_university', 'degree')
    ordering = ('college_university',)


class LanguageSkillAdmin(admin.ModelAdmin):
    list_display = ('language', 'speaking_proficiency', 'writing_proficiency', 'reading_proficiency')
    search_fields = ('language',)
    ordering = ('language',)


class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certification_license', 'institution', 'effective_date')
    search_fields = ('certification_license', 'institution')
    ordering = ('certification_license',)


class HonorAwardAdmin(admin.ModelAdmin):
    list_display = ('honor_reward_publication', 'institution', 'issue_date')
    search_fields = ('honor_reward_publication', 'institution')
    ordering = ('honor_reward_publication',)


class FunctionalSkillAdmin(admin.ModelAdmin):
    list_display = ('skill', 'proficiency')
    search_fields = ('skill',)
    ordering = ('skill',)


class DocumentUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'uploaded_at')
    search_fields = ('user__email', 'document_type')
    ordering = ('user', 'document_type')


class WorkItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'work_type', 'title', 'created_at')
    search_fields = ('user__email', 'title', 'work_type')
    list_filter = ('work_type', 'created_at')
    ordering = ('created_at',)


class SwotAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_strengths', 'get_weaknesses', 'get_opportunities', 'get_threats')
    search_fields = ('user__email',)
    ordering = ('user',)

    def get_strengths(self, obj):
        return obj.strengths[:50] if obj.strengths else 'N/A'  # Truncate to 50 characters for display
    get_strengths.short_description = 'Strengths'

    def get_weaknesses(self, obj):
        return obj.weaknesses[:50] if obj.weaknesses else 'N/A'
    get_weaknesses.short_description = 'Weaknesses'

    def get_opportunities(self, obj):
        return obj.opportunities[:50] if obj.opportunities else 'N/A'
    get_opportunities.short_description = 'Opportunities'

    def get_threats(self, obj):
        return obj.threats[:50] if obj.threats else 'N/A'
    get_threats.short_description = 'Threats'


class SubGoalInline(admin.TabularInline):
    model = SubGoal
    extra = 1


# MainGoal Admin
class MainGoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'start_date', 'end_date', 'status')
    inlines = [SubGoalInline]
    search_fields = ('name',)
    ordering = ('start_date',)


class HabitAdmin(admin.ModelAdmin):
    list_display = ('name',  'frequency', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('created_at',)


class QuizInline(admin.TabularInline):
    model = Quiz
    extra = 1  # Number of empty forms to display

class VideoLectureInline(admin.TabularInline):
    model = VideoLecture
    extra = 1  # Number of empty forms to display

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'description')
    inlines = [VideoLectureInline]

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.instructor != request.user and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj=obj)

class VideoLectureAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'video_file', 'description')
    inlines = [QuizInline]

# Register the models with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PersonalInformation, PersonalInformationAdmin)
admin.site.register(GlobalInformation, GlobalInformationAdmin)
admin.site.register(TechnicalSkill, TechnicalSkillAdmin)
admin.site.register(ProfessionalInformation, ProfessionalInformationAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(LanguageSkill, LanguageSkillAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(HonorsAwardsPublications, HonorAwardAdmin)
admin.site.register(FunctionalSkill, FunctionalSkillAdmin)
admin.site.register(DocumentUpload, DocumentUploadAdmin)
admin.site.register(WorkItem, WorkItemAdmin)
admin.site.register(SwotAnalysis, SwotAnalysisAdmin)
admin.site.register(MainGoal, MainGoalAdmin)
admin.site.register(Strength)
admin.site.register(Weakness)
admin.site.register(Opportunity)
admin.site.register(Threat)
admin.site.register(Course, CourseAdmin)

admin.site.register(Habit, HabitAdmin)