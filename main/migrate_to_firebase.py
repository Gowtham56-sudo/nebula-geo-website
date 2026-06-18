import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebula_geo.settings')
django.setup()

from main.models import Service, PortfolioProject, InternshipProgram, ContactMessage, InternshipApplication, TeamMember, Testimonial
from main.firebase_config import db

def migrate():
    if db is None:
        print("Firebase client is not initialized. Please configure credentials (firebase-key.json or env variable).")
        return

    print("Starting migration to Firestore...")

    # 1. Services
    print("Migrating Services...")
    for item in Service.objects.all():
        db.collection('services').document(str(item.id)).set({
            'title': item.title,
            'description': item.description,
            'icon': item.icon,
            'order': item.order,
            'is_active': item.is_active,
            'created_at': item.created_at.isoformat() if item.created_at else None
        })
    
    # 2. PortfolioProjects
    print("Migrating Portfolio Projects...")
    for item in PortfolioProject.objects.all():
        db.collection('portfolio_projects').document(str(item.id)).set({
            'title': item.title,
            'description': item.description,
            'category': item.category,
            'tech_stack': item.tech_stack,
            'image_url': item.image_url,
            'project_url': item.project_url,
            'is_featured': item.is_featured,
            'order': item.order,
            'created_at': item.created_at.isoformat() if item.created_at else None
        })

    # 3. InternshipPrograms
    print("Migrating Internship Programs...")
    for item in InternshipProgram.objects.all():
        db.collection('internship_programs').document(str(item.id)).set({
            'title': item.title,
            'description': item.description,
            'duration': item.duration,
            'stipend': item.stipend,
            'skills': item.skills,
            'is_active': item.is_active,
            'order': item.order
        })

    # 4. ContactMessages
    print("Migrating Contact Messages...")
    for item in ContactMessage.objects.all():
        db.collection('contact_messages').document(str(item.id)).set({
            'name': item.name,
            'email': item.email,
            'phone': item.phone,
            'subject': item.subject,
            'message': item.message,
            'service_interested': item.service_interested,
            'status': item.status,
            'created_at': item.created_at.isoformat() if item.created_at else None,
            'ip_address': item.ip_address
        })

    # 5. InternshipApplications
    print("Migrating Internship Applications...")
    for item in InternshipApplication.objects.all():
        db.collection('internship_applications').document(str(item.id)).set({
            'name': item.name,
            'email': item.email,
            'phone': item.phone,
            'college': item.college,
            'department': item.department,
            'year': item.year,
            'internship_program': item.internship_program,
            'skills': item.skills,
            'message': item.message,
            'created_at': item.created_at.isoformat() if item.created_at else None
        })

    # 6. TeamMembers
    print("Migrating Team Members...")
    for item in TeamMember.objects.all():
        db.collection('team_members').document(str(item.id)).set({
            'name': item.name,
            'designation': item.designation,
            'bio': item.bio,
            'linkedin_url': item.linkedin_url,
            'order': item.order,
            'is_active': item.is_active
        })

    # 7. Testimonials
    print("Migrating Testimonials...")
    for item in Testimonial.objects.all():
        db.collection('testimonials').document(str(item.id)).set({
            'client_name': item.client_name,
            'client_company': item.client_company,
            'message': item.message,
            'rating': item.rating,
            'is_active': item.is_active,
            'created_at': item.created_at.isoformat() if item.created_at else None
        })

    print("Migration finished successfully!")

if __name__ == '__main__':
    migrate()
