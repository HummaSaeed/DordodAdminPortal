from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter
from .views import (
    DocumentUploadViewSet,
    RegisterView,
    LoginView,
    PersonalInformationView,
    GlobalInformationView,
    SWOTAnalysisDetailView,
    SwotAnalysisViewSet,
    MainGoalViewSet,
    SubGoalViewSet,
    CourseViewSet,
    VideoLectureViewSet,
    QuizViewSet,
    GlobalInformationDetailView,
    LanguageSkillViewSet,
    WorkExperienceViewSet,
    PreviousExperienceViewSet,
    CertificateViewSet,
    ProfessionalInformationViewSet,
    EducationViewSet,
    HonorsAwardsPublicationsViewSet,
    FunctionalSkillViewSet,
    TechnicalSkillViewSet,
    StrengthViewSet,
    WeaknessViewSet,
    OpportunityViewSet,
    ThreatViewSet,
    HabitViewSet,
    UserSettingsView,
    change_password,
)

router = DefaultRouter()
router.register(r'documents', DocumentUploadViewSet, basename='documents')
router.register(r'swot', SwotAnalysisViewSet, basename='swot')
router.register(r'main-goals', MainGoalViewSet, basename='main-goal')
router.register(r'sub-goals', SubGoalViewSet, basename='sub-goal')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'video-lectures', VideoLectureViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'professional-info', ProfessionalInformationViewSet, basename='professional-info')
router.register(r'work-experiences', WorkExperienceViewSet, basename='work-experience')
router.register(r'previous-experiences', PreviousExperienceViewSet, basename='previous-experience')
router.register(r'educations', EducationViewSet, basename='education')
router.register(r'language-skills', LanguageSkillViewSet, basename='language-skill')
router.register(r'certificates', CertificateViewSet, basename='certificate')
router.register(r'honors-awards', HonorsAwardsPublicationsViewSet, basename='honors-awards')
router.register(r'functional-skills', FunctionalSkillViewSet, basename='functional-skill')
router.register(r'technical-skills', TechnicalSkillViewSet, basename='technical-skill')
router.register(r'strengths', StrengthViewSet, basename='strength')
router.register(r'weaknesses', WeaknessViewSet, basename='weakness')
router.register(r'opportunities', OpportunityViewSet, basename='opportunity')
router.register(r'threats', ThreatViewSet, basename='threat')
router.register(r'habits', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include(router.urls)), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('personal-info/', PersonalInformationView.as_view(), name='personal-info'),
    path('global-info/', GlobalInformationView.as_view(), name='global-info-list-create'),
    path('global-info/<int:pk>/', GlobalInformationDetailView.as_view(), name='global-info-detail'),
    path('settings/', UserSettingsView.as_view(), name='user-settings'),
    path('change-password/', change_password, name='change-password'),
]
