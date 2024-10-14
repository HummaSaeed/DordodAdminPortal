from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login as auth_login
from .serializers import (
    RegisterSerializer, 
    LoginSerializer,
    PersonalInformationSerializer,
    GlobalInformationSerializer,
    ProfessionalInformationSerializer,
    DocumentUploadSerializer,
    WorkItemSerializer,
    SWOTAnalysisSerializer,
    MainGoalSerializer,
    SubGoalSerializer,
    CourseSerializer,
    HabitSerializer
)
from .models import CustomUser,Habit, PersonalInformation, GlobalInformation, ProfessionalInformation, DocumentUpload,WorkItem,SwotAnalysis,MainGoal,SubGoal,Course

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
        auth_login(request, user)
        return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)


# Personal Information Views
class PersonalInformationView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonalInformationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Assumes there is a one-to-one relationship with CustomUser
        return PersonalInformation.objects.get(user=self.request.user)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        personal_info = self.get_object()
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
        # Only return documents for the current authenticated user
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class WorkItemViewSet(viewsets.ModelViewSet):
    serializer_class = WorkItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return work items for the current authenticated user
        return WorkItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save work item with the current user
        serializer.save(user=self.request.user)
class SWOTAnalysisListCreateView(generics.ListCreateAPIView):
    queryset = SwotAnalysis.objects.all()
    serializer_class = SWOTAnalysisSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Optionally, you can set the user if the model tracks the user
        serializer.save()

# Retrieve, Update, Delete SWOTAnalysis
class SWOTAnalysisDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SwotAnalysis.objects.all()
    serializer_class = SWOTAnalysisSerializer
    permission_classes = [IsAuthenticated]

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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def purchase(self, request, pk=None):
        course = self.get_object()
        user = request.user

        if user in course.purchasers.all():
            return Response({'detail': 'You have already purchased this course.'}, status=status.HTTP_400_BAD_REQUEST)

        course.purchasers.add(user)
        course.save()

        return Response({'detail': 'Course purchased successfully!'}, status=status.HTTP_200_OK)
class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer