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
    Habit,
    Strength,
    Opportunity,
    Threat,
    Weakness,
    Quiz,
    VideoLecture
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
            'organization_name', 'organization_location', 'duration', 'is_current', 
            'start_date', 'end_date', 'description'
        )

class PreviousExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousExperience
        fields = (
            'title', 'company_name', 'start_date', 'end_date', 'job_responsibilities'
        )

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = (
            'college_university', 'degree', 'area_of_study', 'degree_completed', 'date_completed'
        )
class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

class LanguageSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageSkill
        fields = (
            'language', 'speaking_proficiency', 'writing_proficiency', 'reading_proficiency'
        )

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = (
            'certification_license', 'description', 'institution', 
            'effective_date', 'expiration_date', 'attachment'
        )

class HonorsAwardsPublicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HonorsAwardsPublications
        fields = (
            'honor_reward_publication', 'description', 'institution', 'issue_date', 'attachment'
        )

class FunctionalSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctionalSkill
        fields = ('skill', 'proficiency')

class TechnicalSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSkill
        fields = ('skill', 'proficiency')

class ProfessionalInformationSerializer(serializers.ModelSerializer):
    work_experience = WorkExperienceSerializer(many=True)
    previous_experience = PreviousExperienceSerializer(many=True)
    education = EducationSerializer(many=True)
    language_skill = LanguageSkillSerializer(many=True)
    certificates = CertificateSerializer(many=True)
    honors_awards_publications = HonorsAwardsPublicationsSerializer(many=True)
    functional_skills = FunctionalSkillSerializer(many=True)
    technical_skills = TechnicalSkillSerializer(many=True)

    class Meta:
        model = ProfessionalInformation
        fields = (
            'work_experience', 'previous_experience', 'education',
            'language_skill', 'certificates', 'honors_awards_publications',
            'functional_skills', 'technical_skills'
        )

    def create(self, validated_data):
        # Handle nested objects
        work_experience_data = validated_data.pop('work_experience', [])
        previous_experience_data = validated_data.pop('previous_experience', [])
        education_data = validated_data.pop('education', [])
        language_skill_data = validated_data.pop('language_skill', [])
        certificates_data = validated_data.pop('certificates', [])
        honors_awards_publications_data = validated_data.pop('honors_awards_publications', [])
        functional_skills_data = validated_data.pop('functional_skills', [])
        technical_skills_data = validated_data.pop('technical_skills', [])

        # Create main instance
        professional_info = ProfessionalInformation.objects.create(**validated_data)

        # Create nested objects
        self._create_or_update_nested_objects(professional_info, 'work_experience', work_experience_data)
        self._create_or_update_nested_objects(professional_info, 'previous_experience', previous_experience_data)
        self._create_or_update_nested_objects(professional_info, 'education', education_data)
        self._create_or_update_nested_objects(professional_info, 'language_skill', language_skill_data)
        self._create_or_update_nested_objects(professional_info, 'certificates', certificates_data)
        self._create_or_update_nested_objects(professional_info, 'honors_awards_publications', honors_awards_publications_data)
        self._create_or_update_nested_objects(professional_info, 'functional_skills', functional_skills_data)
        self._create_or_update_nested_objects(professional_info, 'technical_skills', technical_skills_data)

        return professional_info

    def update(self, instance, validated_data):
        # Handle nested objects
        work_experience_data = validated_data.pop('work_experience', [])
        previous_experience_data = validated_data.pop('previous_experience', [])
        education_data = validated_data.pop('education', [])
        language_skill_data = validated_data.pop('language_skill', [])
        certificates_data = validated_data.pop('certificates', [])
        honors_awards_publications_data = validated_data.pop('honors_awards_publications', [])
        functional_skills_data = validated_data.pop('functional_skills', [])
        technical_skills_data = validated_data.pop('technical_skills', [])

        # Update main instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update nested objects
        self._create_or_update_nested_objects(instance, 'work_experience', work_experience_data)
        self._create_or_update_nested_objects(instance, 'previous_experience', previous_experience_data)
        self._create_or_update_nested_objects(instance, 'education', education_data)
        self._create_or_update_nested_objects(instance, 'language_skill', language_skill_data)
        self._create_or_update_nested_objects(instance, 'certificates', certificates_data)
        self._create_or_update_nested_objects(instance, 'honors_awards_publications', honors_awards_publications_data)
        self._create_or_update_nested_objects(instance, 'functional_skills', functional_skills_data)
        self._create_or_update_nested_objects(instance, 'technical_skills', technical_skills_data)

        return instance

    def _create_or_update_nested_objects(self, instance, field_name, nested_data):
        model_class = getattr(instance, field_name).model
        for item in nested_data:
            item_id = item.get('id')
            if item_id:
                obj = model_class.objects.get(id=item_id)
                for attr, value in item.items():
                    setattr(obj, attr, value)
                obj.save()
            else:
                model_class.objects.create(**item, professional_info=instance)
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

class WeaknessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weakness
        fields = ['id', 'description']

class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = ['id', 'description']

class ThreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threat
        fields = ['id', 'description']

class SwotAnalysisSerializer(serializers.ModelSerializer):
    strengths = StrengthSerializer(many=True)
    weaknesses = WeaknessSerializer(many=True)
    opportunities = OpportunitySerializer(many=True)
    threats = ThreatSerializer(many=True)

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
class CourseSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'price', 'discount_percentage', 'discount_start_date', 
            'discount_end_date', 'final_price'
        ]

    def get_final_price(self, obj):
        return obj.discounted_price
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'video_lecture', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']

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
