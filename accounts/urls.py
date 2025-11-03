from django.urls import path
from .views import SignupView, LoginView, AdminLoginView, UserLoginView, ProfileView, ChatbotView, ReportView, AllReportsView, UserReportsView, VerifyReportView, LeaderboardView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('chatbot/', ChatbotView.as_view(), name='chatbot'),
    path('reports/', ReportView.as_view(), name='reports'),
    path('reports/all/', AllReportsView.as_view(), name='all_reports'),
    path('reports/user/', UserReportsView.as_view(), name='user_reports'),
    path('reports/verify/<int:report_id>/', VerifyReportView.as_view(), name='verify_report'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]
