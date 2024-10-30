from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer, 
    LoginSerializer,
    PersonalInformationSerializer,
    GlobalInformationSerializer,
    ProfessionalInformationSerializer,
    DocumentUploadSerializer,
    WorkItemSerializer,
    SwotAnalysisSerializer,
    MainGoalSerializer,
    SubGoalSerializer,
    CourseSerializer,
    HabitSerializer,
    QuizSerializer,
    VideoLectureSerializer
)
from .models import CustomUser,Quiz,VideoLecture, Habit, PersonalInformation, GlobalInformation, ProfessionalInformation, DocumentUpload, WorkItem, SwotAnalysis, MainGoal, SubGoal, Course

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
        return PersonalInformation.objects.get(user=self.request.user)

    def put(self, request, *args, **kwargs):
        personal_info = self.get_object()
        serializer = self.get_serializer(personal_info, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(personal_info, serializer.validated_data)
        return Response(serializer.data)
        
    def perform_update(self, instance, validated_data):
        serializer = self.get_serializer(instance, data=validated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


# Global Information Views
class GlobalInformationView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GlobalInformationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return GlobalInformation.objects.get(user=self.request.user)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        global_info = self.get_object()
        self.perform_update(global_info, serializer.validated_data)
        return Response(serializer.data)

    def perform_update(self, instance, validated_data):
        serializer = self.get_serializer(instance, data=validated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


# Professional Information Views
class ProfessionalInformationView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfessionalInformationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return ProfessionalInformation.objects.get(user=self.request.user)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        professional_info = self.get_object()
        self.perform_update(professional_info, serializer.validated_data)
        return Response(serializer.data)

    def perform_update(self, instance, validated_data):
        serializer = self.get_serializer(instance, data=validated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def purchase(self, request, pk=None):
        course = self.get_object()
        user = request.user
        
        # Check if the user already purchased the course
        if user in course.purchasers.all():
            return Response({'detail': 'You have already purchased this course.'}, status=status.HTTP_400_BAD_REQUEST)

        # Apply discount if available and simulate purchase
        final_price = course.discounted_price or course.price  # Assuming `discounted_price` is a field or method
        # Simulate payment process
        course.purchasers.add(user)
        return Response({'detail': f'Course purchased successfully for {final_price}!'}, status=status.HTTP_200_OK)
class VideoLectureViewSet(viewsets.ModelViewSet):
    queryset = VideoLecture.objects.all()
    serializer_class = VideoLectureSerializer

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only retrieve habits for the currently authenticated user
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save with the current user
        serializer.save(user=self.request.user)