from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    WorkExperience,
    PreviousExperience,
    Education,
    LanguageSkill,
    Certificate,
    HonorsAwardsPublications,
    FunctionalSkill,
    TechnicalSkill,
    GlobalInformation,
    PersonalInformation,
    ProfessionalInformation,
    CustomUser,
    DocumentUpload,
    WorkItem,
    SwotAnalysis,
    MainGoal,
    SubGoal,
    Course,
    Strength,
    Opportunity,
    Threat,
    Weakness,
    Quiz,
    VideoLecture,
    Habit,
    UserSettings
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# CustomUser serializers
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'confirm_password', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        
        # Validate password strength
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
            
        return data

    def create(self, validated_data):
        # Remove confirm_password from the data
        validated_data.pop('confirm_password')
        
        # Generate username from email
        email = validated_data['email']
        base_username = email.split('@')[0]
        username = base_username
        
        # Make username unique by adding numbers if needed
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # Create user with generated username
        user = CustomUser.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError({
                'error': 'Invalid email or password'
            })
        if not user.is_active:
            raise serializers.ValidationError({
                'error': 'User account is disabled'
            })
        data['user'] = user
        return data

# Personal Information serializer
class PersonalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInformation
        fields = [
            'id',
            'profile_picture',
            'first_name',
            'middle_name',
            'last_name',
            'preferred_full_name',
            'email',
            'phone_number',
            'nationality',
            'date_of_birth',
            'birth_name',
            'marital_status',
            'suffix',
            'gender',
            'country',
            'state',
            'city',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        return PersonalInformation.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# Global Information serializer
class GlobalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalInformation
        fields = [
            'id',
            'nationality',
            'current_location',
            'languages',
            'time_zone',
            'availability',
            'preferred_communication',
            'social_media_links',
            'hobbies_interests',
            'volunteer_work',
            'travel_experience',
            'cultural_background',
            'dietary_preferences',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # Get the user from the request context
        user = self.context['request'].user
        
        # Create GlobalInformation instance with the user
        global_info = GlobalInformation.objects.create(
            user=user,
            **validated_data
        )
        return global_info

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# Professional Information serializers
class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = (
            'id',
            'organization_name',
            'organization_location',
            'duration',
            'is_current',
            'start_date',
            'end_date',
            'description'
        )

class PreviousExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousExperience
        fields = (
            'id',
            'title',
            'company_name',
            'start_date',
            'end_date',
            'job_responsibilities'
        )

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = (
            'id',
            'college_university',
            'degree',
            'area_of_study',
            'degree_completed',
            'date_completed'
        )

class LanguageSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageSkill
        fields = (
            'id',
            'language',
            'speaking_proficiency',
            'writing_proficiency',
            'reading_proficiency'
        )

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = (
            'id',
            'certification_license',
            'description',
            'institution',
            'effective_date',
            'expiration_date',
            'attachment'
        )

class HonorsAwardsPublicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HonorsAwardsPublications
        fields = (
            'id',
            'honor_reward_publication',
            'description',
            'institution',
            'issue_date',
            'attachment'
        )

class FunctionalSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctionalSkill
        fields = (
            'id',
            'skill',
            'proficiency'
        )

class TechnicalSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSkill
        fields = (
            'id',
            'skill',
            'proficiency'
        )

class ProfessionalInformationSerializer(serializers.ModelSerializer):
    work_experiences = WorkExperienceSerializer(many=True, read_only=True)
    previous_experiences = PreviousExperienceSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    language_skills = LanguageSkillSerializer(many=True, read_only=True)
    certificates = CertificateSerializer(many=True, read_only=True)
    honors_awards_publications = HonorsAwardsPublicationsSerializer(many=True, read_only=True)
    functional_skills = FunctionalSkillSerializer(many=True, read_only=True)
    technical_skills = TechnicalSkillSerializer(many=True, read_only=True)

    class Meta:
        model = ProfessionalInformation
        fields = [
            'id',
            'user',
            'work_experiences',
            'previous_experiences',
            'educations',
            'language_skills',
            'certificates',
            'honors_awards_publications',
            'functional_skills',
            'technical_skills'
        ]
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        # Handle nested data if needed
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentUpload
        fields = ['document_type', 'document']

    def validate(self, data):
        # Add any additional validation logic here
        return data    
class WorkItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkItem
        fields = ['id', 'work_type', 'title', 'description', 'created_at', 'updated_at']

    def validate(self, data):
        # Add any additional validation for each type of work if necessary
        return data

class StrengthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strength
        fields = ['id', 'description']
        read_only_fields = ['swot_analysis']

class WeaknessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weakness
        fields = ['id', 'description']
        read_only_fields = ['swot_analysis']

class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = ['id', 'description']
        read_only_fields = ['swot_analysis']

class ThreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threat
        fields = ['id', 'description']
        read_only_fields = ['swot_analysis']

class SwotAnalysisSerializer(serializers.ModelSerializer):
    strengths = StrengthSerializer(many=True, read_only=True)
    weaknesses = WeaknessSerializer(many=True, read_only=True)
    opportunities = OpportunitySerializer(many=True, read_only=True)
    threats = ThreatSerializer(many=True, read_only=True)

    class Meta:
        model = SwotAnalysis
        fields = ['id', 'user', 'strengths', 'weaknesses', 'opportunities', 'threats']
        read_only_fields = ['user']

    def _create_items(self, swot_analysis, items_data, model_class):
        for item in items_data:
            # Handle both string and dictionary formats
            description = item if isinstance(item, str) else item.get('description', '')
            model_class.objects.create(
                swot_analysis=swot_analysis,
                description=description
            )

    def create(self, validated_data):
        # Create SwotAnalysis instance
        swot_analysis = SwotAnalysis.objects.create(user=self.context['request'].user)

        # Get nested data from the request data
        request_data = self.context['request'].data

        # Create components if provided
        if 'strengths' in request_data:
            self._create_items(swot_analysis, request_data['strengths'], Strength)

        if 'weaknesses' in request_data:
            self._create_items(swot_analysis, request_data['weaknesses'], Weakness)

        if 'opportunities' in request_data:
            self._create_items(swot_analysis, request_data['opportunities'], Opportunity)

        if 'threats' in request_data:
            self._create_items(swot_analysis, request_data['threats'], Threat)

        return swot_analysis

    def update(self, instance, validated_data):
        request_data = self.context['request'].data

        # Update strengths
        if 'strengths' in request_data:
            instance.strengths.all().delete()
            self._create_items(instance, request_data['strengths'], Strength)

        # Update weaknesses
        if 'weaknesses' in request_data:
            instance.weaknesses.all().delete()
            self._create_items(instance, request_data['weaknesses'], Weakness)

        # Update opportunities
        if 'opportunities' in request_data:
            instance.opportunities.all().delete()
            self._create_items(instance, request_data['opportunities'], Opportunity)

        # Update threats
        if 'threats' in request_data:
            instance.threats.all().delete()
            self._create_items(instance, request_data['threats'], Threat)

        return instance

class MainGoalSerializer(serializers.ModelSerializer):
    subgoals = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = MainGoal
        fields = ['id', 'name', 'description', 'category', 'start_date', 'end_date', 'status', 'weightage', 'subgoals']

# SubGoal Serializer
class SubGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubGoal
        fields = ['id', 'main_goal', 'name', 'description', 'start_date', 'end_date', 'status', 'required_effort', 'spent_effort', 'coach', 'accomplishment']

# First define QuizSerializer since it's used by VideoLectureSerializer
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'video_lecture', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']

# Then define VideoLectureSerializer since it's used by CourseSerializer
class VideoLectureSerializer(serializers.ModelSerializer):
    quizzes = QuizSerializer(many=True, required=False)

    class Meta:
        model = VideoLecture
        fields = ['id', 'course', 'title', 'video_file', 'description', 'quizzes']

    def create(self, validated_data):
        quizzes_data = validated_data.pop('quizzes', [])
        video_lecture = VideoLecture.objects.create(**validated_data)
        for quiz_data in quizzes_data:
            Quiz.objects.create(video_lecture=video_lecture, **quiz_data)
        return video_lecture

# Finally define CourseSerializer which uses VideoLectureSerializer
class CourseSerializer(serializers.ModelSerializer):
    course_lectures = VideoLectureSerializer(many=True, read_only=True)
    final_price = serializers.SerializerMethodField()
    is_purchased = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 
            'title', 
            'description',
            'instructor',
            'start_date',
            'end_date',
            'credit_hours',
            'price',
            'discounted_price',
            'is_active',
            'course_lectures',
            'final_price',
            'is_purchased'
        ]

    def get_final_price(self, obj):
        return float(obj.final_price)

    def get_is_purchased(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.purchasers.filter(id=request.user.id).exists()
        return False

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            'id',
            'name',
            'category',
            'frequency',
            'priority',
            'description',
            'target_value',
            'unit',
            'reminder_time',
            'created_at',
            'updated_at',
            'is_active',
            'streak',
            'last_completed'
        ]
        read_only_fields = ['created_at', 'updated_at', 'streak', 'last_completed']

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        
        # Validate password strength
        try:
            validate_password(attrs['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({
                "new_password": list(e.messages)
            })
        
        return attrs

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = [
            'id',
            'email_notifications',
            'push_notifications',
            'reminder_time',
            'dark_mode',
            'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return UserSettings.objects.create(user=user, **validated_data)
