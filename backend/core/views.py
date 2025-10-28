from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Category, Question, UserProfile, Score, Challenge
from .serializers import (
    CategorySerializer, QuestionSerializer, QuestionDetailSerializer,
    UserSerializer, UserProfileSerializer, RegisterSerializer,
    ScoreSerializer, ChallengeSerializer, AnswerSubmissionSerializer,
    AdminQuestionSerializer, AdminUserSerializer, AdminCategorySerializer
)
from .permissions import IsAdminRole, IsAdminOrReadOnly, IsUserRole


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=True, methods=['get'])
    def questions(self, request, slug=None):
        category = self.get_object()
        questions = category.questions.all()
        
        # Filter by difficulty if provided
        difficulty = request.query_params.get('difficulty')
        if difficulty:
            questions = questions.filter(difficulty=difficulty.upper())
        
        # Filter by question type
        question_type = request.query_params.get('type')
        if question_type:
            questions = questions.filter(question_type=question_type.upper())
        
        # Limit results
        limit = request.query_params.get('limit')
        if limit:
            try:
                questions = questions[:int(limit)]
            except ValueError:
                pass
        
        serializer = QuestionDetailSerializer(questions, many=True)
        return Response(serializer.data)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuestionDetailSerializer
        return QuestionSerializer
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def submit(self, request, pk=None):
        # Only users (not admins) can submit answers
        if hasattr(request.user, 'profile') and request.user.profile.is_admin():
            return Response(
                {'error': 'Admins cannot submit quiz answers'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        question = self.get_object()
        serializer = AnswerSubmissionSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        time_taken = data.get('time_taken', 0)
        is_correct = False
        points_awarded = 0
        
        # Evaluate answer based on question type
        if question.question_type == 'MCQ':
            try:
                submitted_answer = int(data.get('answer', -1))
                is_correct = submitted_answer == question.correct_option
            except (ValueError, TypeError):
                is_correct = False
        
        elif question.question_type == 'QUICK':
            submitted_answer = data.get('answer', '').strip().lower()
            correct_answer = (question.correct_answer or '').strip().lower()
            is_correct = submitted_answer == correct_answer
        
        elif question.question_type == 'CODING':
            # Simple pattern matching for coding questions
            submitted_code = data.get('code', '').strip()
            solution_code = (question.solution_code or '').strip()
            # For demo purposes, check if key parts of solution are present
            if solution_code and submitted_code:
                # Very basic check - in production, use a proper code evaluator
                is_correct = len(submitted_code) > 10  # Placeholder logic
        
        # Award points if correct
        if is_correct:
            points_awarded = question.points
            # Bonus points for speed (if answered in under 30 seconds)
            if time_taken < 30:
                points_awarded = int(points_awarded * 1.2)
        
        # Save score
        score = Score.objects.create(
            user=request.user,
            question=question,
            points_awarded=points_awarded,
            time_taken=time_taken,
            is_correct=is_correct,
            submitted_answer=data.get('answer') or data.get('code', '')[:500]
        )
        
        # Update user profile points
        profile = request.user.profile
        profile.total_points += points_awarded
        profile.save()
        
        return Response({
            'correct': is_correct,
            'points_awarded': points_awarded,
            'time_taken': time_taken,
            'total_points': profile.total_points,
            'explanation': question.explanation if is_correct else None
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserProfileSerializer(request.user.profile)
    return Response(serializer.data)


@api_view(['GET'])
def leaderboard(request):
    period = request.query_params.get('period', 'overall')
    
    # Calculate date filter based on period
    if period == 'daily':
        start_date = timezone.now() - timedelta(days=1)
    elif period == 'weekly':
        start_date = timezone.now() - timedelta(weeks=1)
    else:
        start_date = None
    
    # Get user profiles with points, excluding admins
    profiles = UserProfile.objects.select_related('user').filter(role='user').all()
    
    if start_date:
        # Calculate points for the period
        users_with_points = []
        for profile in profiles:
            period_points = Score.objects.filter(
                user=profile.user,
                created_at__gte=start_date
            ).aggregate(total=Sum('points_awarded'))['total'] or 0
            
            users_with_points.append({
                'id': profile.user.id,
                'username': profile.user.username,
                'avatar_url': profile.avatar_url,
                'total_points': period_points,
                'badges': profile.badges
            })
        
        # Sort by period points
        users_with_points.sort(key=lambda x: x['total_points'], reverse=True)
        leaderboard_data = users_with_points[:50]
    else:
        # Overall leaderboard
        profiles = profiles.order_by('-total_points')[:50]
        leaderboard_data = [
            {
                'id': p.user.id,
                'username': p.user.username,
                'avatar_url': p.avatar_url,
                'total_points': p.total_points,
                'badges': p.badges
            }
            for p in profiles
        ]
    
    return Response({
        'period': period,
        'leaderboard': leaderboard_data
    })


class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Admins shouldn't participate in challenges
        if hasattr(user, 'profile') and user.profile.is_admin():
            return Challenge.objects.none()
        
        return Challenge.objects.filter(
            Q(challenger=user) | Q(opponent=user)
        )
    
    def perform_create(self, serializer):
        # Prevent admins from creating challenges
        if hasattr(self.request.user, 'profile') and self.request.user.profile.is_admin():
            return Response(
                {'error': 'Admins cannot participate in challenges'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(challenger=self.request.user)
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        challenge = self.get_object()
        serializer = self.get_serializer(challenge)
        return Response(serializer.data)


# Admin-only ViewSets for CRUD operations
class AdminQuestionViewSet(viewsets.ModelViewSet):
    """Admin-only viewset for full CRUD on questions with correct answers"""
    queryset = Question.objects.all()
    serializer_class = AdminQuestionSerializer
    permission_classes = [IsAdminRole]
    pagination_class = None  # Disable pagination for admin
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get question statistics"""
        total = Question.objects.count()
        by_type = Question.objects.values('question_type').annotate(count=Count('id'))
        by_difficulty = Question.objects.values('difficulty').annotate(count=Count('id'))
        by_category = Question.objects.values('category__name').annotate(count=Count('id'))
        
        return Response({
            'total_questions': total,
            'by_type': list(by_type),
            'by_difficulty': list(by_difficulty),
            'by_category': list(by_category)
        })


class AdminCategoryViewSet(viewsets.ModelViewSet):
    """Admin-only viewset for full CRUD on categories"""
    queryset = Category.objects.all()
    serializer_class = AdminCategorySerializer
    permission_classes = [IsAdminRole]
    pagination_class = None  # Disable pagination for admin
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get category statistics"""
        categories_with_counts = Category.objects.annotate(
            question_count=Count('questions')
        ).values('id', 'name', 'slug', 'question_count')
        
        return Response({
            'total_categories': Category.objects.count(),
            'categories': list(categories_with_counts)
        })


class AdminUserViewSet(viewsets.ModelViewSet):
    """Admin-only viewset for user management"""
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminRole]
    pagination_class = None  # Disable pagination for admin
    http_method_names = ['get', 'patch', 'delete']  # No POST (use registration), no full PUT
    
    def get_queryset(self):
        # Optionally filter by role
        role = self.request.query_params.get('role')
        if role:
            return User.objects.filter(profile__role=role)
        return User.objects.all()
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user statistics"""
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        admin_count = UserProfile.objects.filter(role='admin').count()
        user_count = UserProfile.objects.filter(role='user').count()
        
        # Recent registrations
        recent = User.objects.order_by('-date_joined')[:10].values(
            'id', 'username', 'email', 'date_joined'
        )
        
        return Response({
            'total_users': total_users,
            'active_users': active_users,
            'admins': admin_count,
            'regular_users': user_count,
            'recent_registrations': list(recent)
        })
    
    @action(detail=True, methods=['patch'])
    def toggle_active(self, request, pk=None):
        """Toggle user active status"""
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        
        return Response({
            'id': user.id,
            'username': user.username,
            'is_active': user.is_active
        })
    
    @action(detail=True, methods=['patch'])
    def change_role(self, request, pk=None):
        """Change user role (admin/user)"""
        user = self.get_object()
        new_role = request.data.get('role')
        
        if new_role not in ['admin', 'user']:
            return Response(
                {'error': 'Invalid role. Must be "admin" or "user"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.profile.role = new_role
        user.profile.save()
        
        return Response({
            'id': user.id,
            'username': user.username,
            'role': user.profile.role
        })


@api_view(['GET'])
@permission_classes([IsAdminRole])
def admin_dashboard_stats(request):
    """Get overall platform statistics for admin dashboard"""
    total_users = User.objects.count()
    total_questions = Question.objects.count()
    total_categories = Category.objects.count()
    total_quiz_attempts = Score.objects.count()
    
    # Recent activity
    recent_scores = Score.objects.select_related('user', 'question').order_by('-created_at')[:10]
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    # Top performers
    top_users = UserProfile.objects.filter(role='user').order_by('-total_points')[:10]
    
    return Response({
        'overview': {
            'total_users': total_users,
            'total_questions': total_questions,
            'total_categories': total_categories,
            'total_quiz_attempts': total_quiz_attempts,
        },
        'recent_scores': ScoreSerializer(recent_scores, many=True).data,
        'recent_users': [{'id': u.id, 'username': u.username, 'date_joined': u.date_joined} for u in recent_users],
        'top_performers': [{'username': p.user.username, 'points': p.total_points} for p in top_users],
    })

