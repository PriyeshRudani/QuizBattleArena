from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'challenges', views.ChallengeViewSet, basename='challenge')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.register_user, name='register'),
    path('user/profile/', views.user_profile, name='user-profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
