from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter
from .views import (
    DocumentUploadViewSet,
    HabitViewSet,
    RegisterView,
    LoginView,
    PersonalInformationView,
    GlobalInformationView,
    ProfessionalInformationView,
    SWOTAnalysisDetailView,
    SwotAnalysisViewSet,
    MainGoalViewSet,
    SubGoalViewSet,
    HabitViewSet,
    CourseViewSet,
    VideoLectureViewSet,
    QuizViewSet,
    GlobalInformationDetailView
)

router = DefaultRouter()
router.register(r'documents', DocumentUploadViewSet, basename='documents')
router.register(r'swot', SwotAnalysisViewSet, basename='swot')
router.register(r'main-goals', MainGoalViewSet, basename='main-goal')
router.register(r'sub-goals', SubGoalViewSet, basename='sub-goal')
router.register(r'habits', HabitViewSet, basename='habits')
router.register(r'courses', CourseViewSet)
router.register(r'video-lectures', VideoLectureViewSet)
router.register(r'quizzes', QuizViewSet)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)), 
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('personal-info/', PersonalInformationView.as_view(), name='personal-info'),
     path('global-info/', GlobalInformationView.as_view(), name='global-info-list-create'),
    path('global-info/<int:pk>/', GlobalInformationDetailView.as_view(), name='global-info-detail'),
    path('professional-info/', ProfessionalInformationView.as_view(), name='professional-info'),
    # path('document-upload/', DocumentUploadViewSet.as_view(), name='document-upload'),
]
