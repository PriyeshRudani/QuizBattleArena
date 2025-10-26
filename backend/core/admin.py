from django.contrib import admin
from .models import Category, Question, UserProfile, Score, Challenge


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at', 'question_count']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'question_type', 'difficulty', 'language', 'points', 'created_at']
    list_filter = ['question_type', 'difficulty', 'language', 'category', 'created_at']
    search_fields = ['title', 'question_text']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'question_type', 'difficulty', 'language', 'points')
        }),
        ('Question Content', {
            'fields': ('question_text', 'options', 'explanation')
        }),
        ('Answers', {
            'fields': ('correct_option', 'correct_answer', 'solution_code'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_points', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['created_at']


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'points_awarded', 'is_correct', 'time_taken', 'created_at']
    list_filter = ['is_correct', 'created_at']
    search_fields = ['user__username', 'question__title']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['id', 'challenger', 'opponent', 'category', 'status', 'winner', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['challenger__username', 'opponent__username']
    readonly_fields = ['created_at', 'started_at', 'completed_at']
    date_hierarchy = 'created_at'
