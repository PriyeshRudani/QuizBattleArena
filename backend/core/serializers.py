from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Question, UserProfile, Score, Challenge


class CategorySerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'question_count', 'created_at']
        read_only_fields = ['slug', 'created_at']
    
    def get_question_count(self, obj):
        return obj.questions.count()


class QuestionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'title', 'category', 'category_name', 'question_type', 
            'difficulty', 'language', 'question_text', 'options', 
            'explanation', 'points', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Don't expose correct answers in list/retrieve views
        representation.pop('correct_option', None)
        representation.pop('correct_answer', None)
        representation.pop('solution_code', None)
        return representation


class QuestionDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'title', 'category', 'category_name', 'question_type',
            'difficulty', 'language', 'question_text', 'options',
            'points', 'created_at'
        ]


class UserSerializer(serializers.ModelSerializer):
    total_points = serializers.IntegerField(source='profile.total_points', read_only=True)
    badges = serializers.JSONField(source='profile.badges', read_only=True)
    avatar_url = serializers.URLField(source='profile.avatar_url', read_only=True, allow_null=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'total_points', 'badges', 'avatar_url', 'date_joined']
        read_only_fields = ['date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(read_only=True)
    is_admin = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'role', 'is_admin', 'total_points', 'badges', 'avatar_url', 'bio', 'created_at']
        read_only_fields = ['role', 'total_points', 'created_at']
    
    def get_is_admin(self, obj):
        return obj.is_admin()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class ScoreSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    question_title = serializers.CharField(source='question.title', read_only=True)
    
    class Meta:
        model = Score
        fields = ['id', 'user', 'username', 'question', 'question_title', 
                  'points_awarded', 'time_taken', 'is_correct', 'created_at']
        read_only_fields = ['created_at']


class ChallengeSerializer(serializers.ModelSerializer):
    challenger_name = serializers.CharField(source='challenger.username', read_only=True)
    opponent_name = serializers.CharField(source='opponent.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    winner_name = serializers.CharField(source='winner.username', read_only=True, allow_null=True)
    
    class Meta:
        model = Challenge
        fields = [
            'id', 'challenger', 'challenger_name', 'opponent', 'opponent_name',
            'category', 'category_name', 'status', 'winner', 'winner_name',
            'created_at', 'started_at', 'completed_at'
        ]
        read_only_fields = ['created_at', 'started_at', 'completed_at', 'status', 'winner']


class AnswerSubmissionSerializer(serializers.Serializer):
    answer = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(required=False, allow_blank=True)
    language = serializers.CharField(required=False, allow_blank=True)
    time_taken = serializers.IntegerField(required=False, default=0)


# Admin Serializers with full field access
class AdminQuestionSerializer(serializers.ModelSerializer):
    """Full question serializer for admin with correct answers"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'title', 'category', 'category_name', 'question_type',
            'difficulty', 'language', 'question_text', 'options',
            'correct_option', 'correct_answer', 'solution_code',
            'explanation', 'points', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AdminUserSerializer(serializers.ModelSerializer):
    """Full user serializer for admin with role and profile info"""
    role = serializers.CharField(source='profile.role', read_only=True)
    total_points = serializers.IntegerField(source='profile.total_points', read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'role', 'total_points', 'date_joined', 'last_login'
        ]
        read_only_fields = ['date_joined', 'last_login']


class AdminCategorySerializer(serializers.ModelSerializer):
    """Full category serializer for admin with question count"""
    question_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'question_count', 'created_at']
        read_only_fields = ['slug', 'created_at']
    
    def get_question_count(self, obj):
        return obj.questions.count()

