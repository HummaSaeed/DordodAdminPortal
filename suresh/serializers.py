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
    Habit
)

# CustomUser serializers
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'password_confirm')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        return user

    def create(self, validated_data):
        user = authenticate(email=validated_data['email'], password=validated_data['password'])
        if user is None:
            raise serializers.ValidationError('Invalid credentials')

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

# Personal Information serializer
class PersonalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInformation
        fields = [
            'profile_picture',  # New field
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

    def create(self, validated_data):
        return PersonalInformation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# Global Information serializer
class GlobalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalInformation
        fields = (
            'date_learned', 'challenge_group', 'degree_of_challenge', 'type_of_challenge',
            'issuing_authority', 'reference_number', 'religion', 'number_of_children',
            'occupational_code', 'father_husband_guardian_name'
        )

    def create(self, validated_data):
        return GlobalInformation.objects.create(**validated_data)

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

    def create(self, validated_data):
        strengths_data = validated_data.pop('strengths')
        weaknesses_data = validated_data.pop('weaknesses')
        opportunities_data = validated_data.pop('opportunities')
        threats_data = validated_data.pop('threats')

        swot_analysis = SwotAnalysis.objects.create(user=self.context['request'].user)

        # Process related instances
        self._process_nested_objects(swot_analysis, 'strengths', strengths_data)
        self._process_nested_objects(swot_analysis, 'weaknesses', weaknesses_data)
        self._process_nested_objects(swot_analysis, 'opportunities', opportunities_data)
        self._process_nested_objects(swot_analysis, 'threats', threats_data)

        return swot_analysis

    def update(self, instance, validated_data):
        # Clear existing related objects
        instance.strengths.all().delete()
        instance.weaknesses.all().delete()
        instance.opportunities.all().delete()
        instance.threats.all().delete()

        strengths_data = validated_data.pop('strengths')
        weaknesses_data = validated_data.pop('weaknesses')
        opportunities_data = validated_data.pop('opportunities')
        threats_data = validated_data.pop('threats')

        # Process related instances
        self._process_nested_objects(instance, 'strengths', strengths_data, create=True)
        self._process_nested_objects(instance, 'weaknesses', weaknesses_data, create=True)
        self._process_nested_objects(instance, 'opportunities', opportunities_data, create=True)
        self._process_nested_objects(instance, 'threats', threats_data, create=True)

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
