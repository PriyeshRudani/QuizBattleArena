"""
Script to delete all users and create new admin and player accounts
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile

def setup_users():
    print("=" * 60)
    print("Setting up users...")
    print("=" * 60)
    
    # Delete all existing users
    user_count = User.objects.count()
    print(f"\n1. Deleting {user_count} existing users...")
    User.objects.all().delete()
    print("   ✅ All users deleted")
    
    # Create admin user
    print("\n2. Creating admin user...")
    admin = User.objects.create_superuser(
        username='lothar',
        email='lotharaduin@gmail.com',
        password='Admin@123'
    )
    admin.profile.role = 'admin'
    admin.profile.save()
    print(f"   ✅ Admin created: {admin.username} ({admin.email})")
    print(f"      Role: {admin.profile.role}")
    
    # Create player user
    print("\n3. Creating player user...")
    player = User.objects.create_user(
        username='priyesh',
        email='priyeshrudani@gmail.com',
        password='Priyesh@123'
    )
    player.profile.role = 'user'
    player.profile.save()
    print(f"   ✅ Player created: {player.username} ({player.email})")
    print(f"      Role: {player.profile.role}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    print(f"Total users: {User.objects.count()}")
    print(f"Admin users: {UserProfile.objects.filter(role='admin').count()}")
    print(f"Player users: {UserProfile.objects.filter(role='user').count()}")
    print("\n✅ Setup complete!")
    print("\nLogin credentials:")
    print("-" * 60)
    print("Admin:")
    print("  Username: lothar")
    print("  Password: Admin@123")
    print("\nPlayer:")
    print("  Username: priyesh")
    print("  Password: Priyesh@123")
    print("=" * 60)

if __name__ == '__main__':
    setup_users()
