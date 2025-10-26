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
    ScoreSerializer, ChallengeSerializer, AnswerSubmissionSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
    
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
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuestionDetailSerializer
        return QuestionSerializer
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def submit(self, request, pk=None):
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
    
    # Get user profiles with points
    profiles = UserProfile.objects.select_related('user').all()
    
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
        return Challenge.objects.filter(
            Q(challenger=user) | Q(opponent=user)
        )
    
    def perform_create(self, serializer):
        serializer.save(challenger=self.request.user)
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        challenge = self.get_object()
        serializer = self.get_serializer(challenge)
        return Response(serializer.data)
