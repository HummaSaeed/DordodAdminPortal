from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from django.http import Http404
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    PersonalInformationSerializer,
    GlobalInformationSerializer,
    ProfessionalInformationSerializer,
    WorkExperienceSerializer,
    PreviousExperienceSerializer,
    EducationSerializer,
    LanguageSkillSerializer,
    CertificateSerializer,
    HonorsAwardsPublicationsSerializer,
    FunctionalSkillSerializer,
    TechnicalSkillSerializer,
    DocumentUploadSerializer,
    WorkItemSerializer,
    SwotAnalysisSerializer,
    MainGoalSerializer,
    SubGoalSerializer,
    CourseSerializer,
    QuizSerializer,
    VideoLectureSerializer,
    StrengthSerializer,
    WeaknessSerializer,
    OpportunitySerializer,
    ThreatSerializer,
    HabitSerializer,
)
from .models import (
    CustomUser,
    PersonalInformation,
    GlobalInformation,
    ProfessionalInformation,
    WorkExperience,
    PreviousExperience,
    Education,
    LanguageSkill,
    Certificate,
    HonorsAwardsPublications,
    FunctionalSkill,
    TechnicalSkill,
    DocumentUpload,
    WorkItem,
    SwotAnalysis,
    MainGoal,
    SubGoal,
    Course,
    Quiz,
    VideoLecture,
    Strength,
    Weakness,
    Opportunity,
    Threat,
    Habit,
)
from datetime import datetime, timedelta
from django.utils import timezone

# User Registration View
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

# User Login View
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        
        # Create JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


# Personal Information Views
class PersonalInformationView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonalInformationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return PersonalInformation.objects.get(user=self.request.user)
        except PersonalInformation.DoesNotExist:
            # Create a new PersonalInformation object if it doesn't exist
            return PersonalInformation.objects.create(
                user=self.request.user,
                email=self.request.user.email  # Set default email from user
            )

    def put(self, request, *args, **kwargs):
        try:
            personal_info = self.get_object()
        except PersonalInformation.DoesNotExist:
            personal_info = PersonalInformation.objects.create(
                user=request.user,
                email=request.user.email
            )
        
        serializer = self.get_serializer(personal_info, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer.validated_data)
        return Response(serializer.data)
        
    def perform_update(self, validated_data):
        personal_info = self.get_object()
        for attr, value in validated_data.items():
            setattr(personal_info, attr, value)
        personal_info.save()

class WorkExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkExperience.objects.filter(professional_info__user=self.request.user)

    def perform_create(self, serializer):
        prof_info, _ = ProfessionalInformation.objects.get_or_create(user=self.request.user)
        serializer.save(professional_info=prof_info)

class PreviousExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = PreviousExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PreviousExperience.objects.filter(professional_info__user=self.request.user)

    def perform_create(self, serializer):
        prof_info, _ = ProfessionalInformation.objects.get_or_create(user=self.request.user)
        serializer.save(professional_info=prof_info)

class EducationViewSet(viewsets.ModelViewSet):
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Education.objects.filter(professional_info__user=self.request.user)

    def perform_create(self, serializer):
        prof_info, _ = ProfessionalInformation.objects.get_or_create(user=self.request.user)
        serializer.save(professional_info=prof_info)

class LanguageSkillViewSet(viewsets.ModelViewSet):
    serializer_class = LanguageSkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LanguageSkill.objects.filter(professional_info__user=self.request.user)

    def perform_create(self, serializer):
        prof_info, _ = ProfessionalInformation.objects.get_or_create(user=self.request.user)
        serializer.save(professional_info=prof_info)

class CertificateViewSet(viewsets.ModelViewSet):
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Certificate.objects.filter(professional_info__user=self.request.user)

    def perform_create(self, serializer):
        prof_info, _ = ProfessionalInformation.objects.get_or_create(user=self.request.user)
        serializer.save(professional_info=prof_info)

class HonorsAwardsPublicationsViewSet(viewsets.ModelViewSet):
    serializer_class = HonorsAwardsPublicationsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HonorsAwardsPublications.objects.filter(professional_info__user=self.request.user)

    def perform_create(self, serializer):
        prof_info, _ = ProfessionalInformation.objects.get_or_create(user=self.request.user)
        serializer.save(professional_info=prof_info)

class FunctionalSkillViewSet(viewsets.ModelViewSet):
    serializer_class = FunctionalSkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FunctionalSkill.objects.filter(professional_info__user=self.request.user)

    def perform_create(self, serializer):
        prof_info, _ = ProfessionalInformation.objects.get_or_create(user=self.request.user)
        serializer.save(professional_info=prof_info)

class TechnicalSkillViewSet(viewsets.ModelViewSet):
    serializer_class = TechnicalSkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TechnicalSkill.objects.filter(professional_info__user=self.request.user)

    def perform_create(self, serializer):
        prof_info, _ = ProfessionalInformation.objects.get_or_create(user=self.request.user)
        serializer.save(professional_info=prof_info)

# Global Information Views
class GlobalInformationView(generics.ListCreateAPIView):
    serializer_class = GlobalInformationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GlobalInformation.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            # Try to get existing record
            instance = GlobalInformation.objects.get(user=request.user)
            # Update existing record
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GlobalInformation.DoesNotExist:
            # Create new record if doesn't exist
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GlobalInformationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GlobalInformationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return GlobalInformation.objects.get(user=self.request.user)
        except GlobalInformation.DoesNotExist:
            # Create a new record if it doesn't exist
            return GlobalInformation.objects.create(
                user=self.request.user,
                # Add default values if needed
                date_learned=timezone.now().date(),
                challenge_group='',
                degree_of_challenge='',
                type_of_challenge='',
                issuing_authority='',
                religion='',
                number_of_children=0,
                occupational_code='',
                father_husband_guardian_name=''
            )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "GlobalInformation deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
# Professional Information Views


class ProfessionalInformationViewSet(viewsets.ModelViewSet):
    queryset = ProfessionalInformation.objects.all()
    serializer_class = ProfessionalInformationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        return ProfessionalInformation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if ProfessionalInformation.objects.filter(user=self.request.user).exists():
            raise ValidationError("Professional Information already exists for this user.")
        serializer.save(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.first()
        if not obj:
            raise Http404("Professional Information not found")
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_work_experience(self, request, pk=None):
        professional_info = self.get_object()
        serializer = WorkExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(professional_info=professional_info)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_previous_experience(self, request, pk=None):
        professional_info = self.get_object()
        serializer = PreviousExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(professional_info=professional_info)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_education(self, request, pk=None):
        professional_info = self.get_object()
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(professional_info=professional_info)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_language_skill(self, request, pk=None):
        professional_info = self.get_object()
        serializer = LanguageSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(professional_info=professional_info)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_certificate(self, request, pk=None):
        professional_info = self.get_object()
        serializer = CertificateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(professional_info=professional_info)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_honor_award(self, request, pk=None):
        professional_info = self.get_object()
        serializer = HonorsAwardsPublicationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(professional_info=professional_info)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_functional_skill(self, request, pk=None):
        professional_info = self.get_object()
        serializer = FunctionalSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(professional_info=professional_info)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_technical_skill(self, request, pk=None):
        professional_info = self.get_object()
        serializer = TechnicalSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(professional_info=professional_info)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentUploadViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentUploadSerializer
    queryset = DocumentUpload.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class WorkItemViewSet(viewsets.ModelViewSet):
    serializer_class = WorkItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return work items for the current authenticated user
        return WorkItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save work item with the current user
        serializer.save(user=self.request.user)

class SwotAnalysisViewSet(viewsets.ModelViewSet):
    queryset = SwotAnalysis.objects.all()
    serializer_class = SwotAnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return SWOT analyses for the logged-in user
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set the user to the logged-in user
        serializer.save(user=self.request.user)
# Retrieve, Update, Delete SWOTAnalysis
class SWOTAnalysisDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SwotAnalysis.objects.all()
    serializer_class = SwotAnalysisSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # Retrieve SWOT analysis for the specific logged-in user only
        return SwotAnalysis.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        # Automatically associate the SWOT entry with the logged-in user
        serializer.save(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # This will allow partial updates if PATCH method is used
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class MainGoalViewSet(viewsets.ModelViewSet):
    queryset = MainGoal.objects.all()
    serializer_class = MainGoalSerializer

# SubGoal ViewSet
class SubGoalViewSet(viewsets.ModelViewSet):
    queryset = SubGoal.objects.all()
    serializer_class = SubGoalSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        course = self.get_object()
        user = request.user
        
        if course.purchasers.filter(id=user.id).exists():
            return Response(
                {'detail': 'You have already purchased this course.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        course.purchasers.add(user)
        return Response(
            {'detail': 'Course purchased successfully.'},
            status=status.HTTP_200_OK
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class VideoLectureViewSet(viewsets.ModelViewSet):
    queryset = VideoLecture.objects.all()
    serializer_class = VideoLectureSerializer

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class StrengthViewSet(viewsets.ModelViewSet):
    serializer_class = StrengthSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Strength.objects.filter(swot_analysis__user=self.request.user)

    def perform_create(self, serializer):
        swot_analysis = SwotAnalysis.objects.filter(user=self.request.user).first()
        if not swot_analysis:
            swot_analysis = SwotAnalysis.objects.create(user=self.request.user)
        serializer.save(swot_analysis=swot_analysis)

class WeaknessViewSet(viewsets.ModelViewSet):
    serializer_class = WeaknessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Weakness.objects.filter(swot_analysis__user=self.request.user)

    def perform_create(self, serializer):
        swot_analysis = SwotAnalysis.objects.filter(user=self.request.user).first()
        if not swot_analysis:
            swot_analysis = SwotAnalysis.objects.create(user=self.request.user)
        serializer.save(swot_analysis=swot_analysis)

class OpportunityViewSet(viewsets.ModelViewSet):
    serializer_class = OpportunitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Opportunity.objects.filter(swot_analysis__user=self.request.user)

    def perform_create(self, serializer):
        swot_analysis = SwotAnalysis.objects.filter(user=self.request.user).first()
        if not swot_analysis:
            swot_analysis = SwotAnalysis.objects.create(user=self.request.user)
        serializer.save(swot_analysis=swot_analysis)

class ThreatViewSet(viewsets.ModelViewSet):
    serializer_class = ThreatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Threat.objects.filter(swot_analysis__user=self.request.user)

    def perform_create(self, serializer):
        swot_analysis = SwotAnalysis.objects.filter(user=self.request.user).first()
        if not swot_analysis:
            swot_analysis = SwotAnalysis.objects.create(user=self.request.user)
        serializer.save(swot_analysis=swot_analysis)

class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        habit = self.get_object()
        today = timezone.now().date()

        if habit.last_completed != today:
            if habit.last_completed == today - timedelta(days=1):
                habit.streak += 1
            else:
                habit.streak = 1
            
            habit.last_completed = today
            habit.save()

        return Response({
            'status': 'success',
            'streak': habit.streak,
            'message': 'Habit marked as completed'
        })

    @action(detail=True, methods=['post'])
    def reset_streak(self, request, pk=None):
        habit = self.get_object()
        habit.streak = 0
        habit.save()
        return Response({
            'status': 'success',
            'message': 'Streak reset successfully'
        })