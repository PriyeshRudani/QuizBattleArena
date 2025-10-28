"""Check questions in database"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from core.models import Question, Category

print("=" * 60)
print("Database Questions Status")
print("=" * 60)

total = Question.objects.count()
print(f"\nTotal questions: {total}")

if total > 0:
    mcq = Question.objects.filter(question_type='MCQ').count()
    code = Question.objects.filter(question_type='CODE').count()
    quick = Question.objects.filter(question_type='QUICK').count()
    
    print(f"  MCQ: {mcq}")
    print(f"  CODE: {code}")
    print(f"  QUICK: {quick}")
    
    print("\nQuestions by category:")
    for cat in Category.objects.all():
        count = Question.objects.filter(category=cat).count()
        print(f"  {cat.name}: {count}")
else:
    print("\n⚠️  No questions found! You need to run the seed command:")
    print("   python manage.py seed_questions")

print("=" * 60)
