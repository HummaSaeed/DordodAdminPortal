from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    PersonalInformationView,
    GlobalInformationView,
    ProfessionalInformationView,
    SWOTAnalysisDetailView,
    SWOTAnalysisListCreateView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('personal-info/', PersonalInformationView.as_view(), name='personal-info'),
    path('global-info/', GlobalInformationView.as_view(), name='global-info'),
    path('professional-info/', ProfessionalInformationView.as_view(), name='professional-info'),
    path('swot/', SWOTAnalysisListCreateView.as_view(), name='swot-list-create'),
    path('swot/<int:pk>/', SWOTAnalysisDetailView.as_view(), name='swot-detail'),
]
