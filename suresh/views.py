from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
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
    UserSettingsSerializer,
    ChangePasswordSerializer,
    WhiteboardSessionSerializer,
    SurveySerializer,
    SurveyResponseSerializer,
    RewardSerializer,
    UserRewardSerializer,
    TimeEntrySerializer,
    NoteSerializer,
    CreditScoreSerializer,
    AssessmentSerializer,
    UserAssessmentSerializer,
    ResumeSerializer,
    WebsiteSerializer,
    PostSerializer,
    ActivitySerializer,
    CoachSerializer,
    CoachRequestSerializer,
    MoodTrackingSerializer,
    AccomplishmentSerializer,
    AccomplishmentShareSerializer,
    UserJobSerializer,
    ConversationSerializer,
    MessageSerializer
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
    UserSettings,
    WhiteboardSession,
    Survey,
    SurveyResponse,
    Reward,
    UserReward,
    TimeEntry,
    Note,
    CreditScore,
    Assessment,
    UserAssessment,
    Resume,
    Website,
    Post,
    Activity,
    Coach,
    CoachRequest,
    MoodTracking,
    Accomplishment,
    AccomplishmentShare,
    UserJob,
    Conversation,
    Message
)
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

# User Registration View
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []  # Allow anyone to register

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Create the user
            user = serializer.save()
            
            # Create PersonalInformation
            PersonalInformation.objects.create(
                user=user,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                preferred_full_name=f"{user.first_name} {user.last_name}".strip()
            )

            # Create UserSettings
            UserSettings.objects.create(user=user)

            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

# User Login View
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = []  # Allow anyone to login

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }, status=status.HTTP_200_OK)


# Personal Information Views
class PersonalInformationView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonalInformationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        personal_info, created = PersonalInformation.objects.get_or_create(
            user=self.request.user,
            defaults={
                'email': self.request.user.email,
                'first_name': self.request.user.first_name,
                'last_name': self.request.user.last_name,
                'preferred_full_name': f"{self.request.user.first_name} {self.request.user.last_name}".strip()
            }
        )
        return personal_info

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(
                {"detail": "Personal Information deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
class GlobalInformationView(generics.RetrieveUpdateAPIView):
    serializer_class = GlobalInformationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get or create the GlobalInformation instance for the current user
        obj, created = GlobalInformation.objects.get_or_create(user=self.request.user)
        return obj

    def post(self, request, *args, **kwargs):
        # Check if GlobalInformation already exists for this user
        try:
            instance = GlobalInformation.objects.get(user=request.user)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        except GlobalInformation.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

class GlobalInformationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GlobalInformationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return GlobalInformation.objects.get(user=self.request.user)
        except GlobalInformation.DoesNotExist:
            return GlobalInformation.objects.create(
                user=self.request.user,
                nationality='',
                current_location='',
                languages='',
                time_zone='',
                availability='',
                preferred_communication='',
                social_media_links='',
                hobbies_interests='',
                volunteer_work='',
                travel_experience='',
                cultural_background='',
                dietary_preferences=''
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

class UserSettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get or create settings for the current user
        settings, created = UserSettings.objects.get_or_create(user=self.request.user)
        return settings

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    
    if serializer.is_valid():
        user = request.user
        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']

        # Check current password
        if not user.check_password(current_password):
            return Response(
                {'current_password': 'Current password is incorrect'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Validate and set new password
            validate_password(new_password, user)
            user.set_password(new_password)
            user.save()

            return Response(
                {'message': 'Password updated successfully'}, 
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {'new_password': e.messages}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Whiteboard Session ViewSet
class WhiteboardSessionViewSet(viewsets.ModelViewSet):
    queryset = WhiteboardSession.objects.all()
    serializer_class = WhiteboardSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

# Survey ViewSet
class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]

class SurveyResponseViewSet(viewsets.ModelViewSet):
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Reward ViewSet
class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = [IsAuthenticated]

class UserRewardViewSet(viewsets.ModelViewSet):
    queryset = UserReward.objects.all()
    serializer_class = UserRewardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Time Entry ViewSet
class TimeEntryViewSet(viewsets.ModelViewSet):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

# Note ViewSet
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

# Credit Score ViewSet
class CreditScoreViewSet(viewsets.ModelViewSet):
    queryset = CreditScore.objects.all()
    serializer_class = CreditScoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

# Assessment ViewSet
class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]

class UserAssessmentViewSet(viewsets.ModelViewSet):
    queryset = UserAssessment.objects.all()
    serializer_class = UserAssessmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Resume ViewSet
class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

# Website ViewSet
class WebsiteViewSet(viewsets.ModelViewSet):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

# Post ViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically set the user


class CoachViewSet(viewsets.ModelViewSet):
    serializer_class = CoachSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            # For listing, return all coaches
            return Coach.objects.all()
        elif self.action == 'retrieve':
            # For retrieving a specific coach
            return Coach.objects.filter(id=self.kwargs.get('pk'))
        else:
            # For other actions, return only the current user's coach profile
            return Coach.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Create coach profile for the current user
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def requests(self, request, pk=None):
        """Get all coaching requests for a specific coach"""
        coach = self.get_object()
        requests = CoachRequest.objects.filter(coach=coach)
        serializer = CoachRequestSerializer(requests, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def handle_request(self, request, pk=None):
        """Handle a coaching request (accept/reject)"""
        coach = self.get_object()
        request_id = request.data.get('request_id')
        action = request.data.get('action')  # 'accept' or 'reject'

        try:
            coach_request = CoachRequest.objects.get(id=request_id, coach=coach)
            if action == 'accept':
                coach_request.status = 'accepted'
            elif action == 'reject':
                coach_request.status = 'rejected'
            else:
                return Response(
                    {'error': 'Invalid action'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            coach_request.save()
            return Response({'status': 'success'})
        except CoachRequest.DoesNotExist:
            return Response(
                {'error': 'Request not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get the current user's coach profile"""
        try:
            coach = Coach.objects.get(user=request.user)
            serializer = self.get_serializer(coach)
            return Response(serializer.data)
        except Coach.DoesNotExist:
            return Response(
                {'error': 'Coach profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class MoodTrackingViewSet(viewsets.ModelViewSet):
    serializer_class = MoodTrackingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return mood entries for the current authenticated user
        return MoodTracking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save mood entry with the current user
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's mood entry for the current user"""
        today = timezone.now().date()
        try:
            mood = MoodTracking.objects.get(user=request.user, date=today)
            serializer = self.get_serializer(mood)
            return Response(serializer.data)
        except MoodTracking.DoesNotExist:
            return Response({'detail': 'No mood entry for today'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get mood history for the current user"""
        moods = MoodTracking.objects.filter(user=request.user).order_by('-date')
        serializer = self.get_serializer(moods, many=True)
        return Response(serializer.data)

class AccomplishmentViewSet(viewsets.ModelViewSet):
    serializer_class = AccomplishmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Accomplishment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """Share an accomplishment on a platform"""
        accomplishment = self.get_object()
        platform = request.data.get('platform')
        message = request.data.get('message', '')

        if not platform:
            return Response(
                {'error': 'Platform is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create share record
        share = AccomplishmentShare.objects.create(
            accomplishment=accomplishment,
            platform=platform,
            message=message
        )

        # Here you would integrate with actual social media APIs
        # For now, we'll just return success
        return Response({
            'message': f'Accomplishment shared on {platform}',
            'share_id': share.id
        })

    @action(detail=False, methods=['get'])
    def public(self, request):
        """Get public accomplishments"""
        accomplishments = Accomplishment.objects.filter(is_public=True)
        serializer = self.get_serializer(accomplishments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get accomplishments grouped by category"""
        category = request.query_params.get('category')
        if category:
            accomplishments = self.get_queryset().filter(category=category)
        else:
            accomplishments = self.get_queryset()

        serializer = self.get_serializer(accomplishments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get accomplishment statistics"""
        queryset = self.get_queryset()
        
        stats = {
            'total': queryset.count(),
            'by_category': {},
            'public_count': queryset.filter(is_public=True).count(),
            'recent': queryset.filter(
                date__gte=timezone.now().date() - timedelta(days=30)
            ).count()
        }

        # Count by category
        for category, _ in Accomplishment.CATEGORY_CHOICES:
            stats['by_category'][category] = queryset.filter(category=category).count()

        return Response(stats)

class AccomplishmentShareViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AccomplishmentShareSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AccomplishmentShare.objects.filter(accomplishment__user=self.request.user)

class UserJobViewSet(viewsets.ModelViewSet):
    serializer_class = UserJobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserJob.objects.filter(user=self.request.user).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        messages = conversation.messages.order_by('created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        conversation = self.get_object()
        conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
        return Response({'status': 'marked as read'})

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)