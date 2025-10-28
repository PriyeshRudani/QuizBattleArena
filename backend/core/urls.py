from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Public and authenticated user routes
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'challenges', views.ChallengeViewSet, basename='challenge')

# Admin-only routes
admin_router = DefaultRouter()
admin_router.register(r'questions', views.AdminQuestionViewSet, basename='admin-question')
admin_router.register(r'categories', views.AdminCategoryViewSet, basename='admin-category')
admin_router.register(r'users', views.AdminUserViewSet, basename='admin-user')

urlpatterns = [
    # Public and user routes
    path('', include(router.urls)),
    path('auth/register/', views.register_user, name='register'),
    path('user/profile/', views.user_profile, name='user-profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    
    # Admin-only routes
    path('admin/', include(admin_router.urls)),
    path('admin/dashboard/stats/', views.admin_dashboard_stats, name='admin-dashboard-stats'),
]
