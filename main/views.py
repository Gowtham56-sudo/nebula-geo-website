

from django.shortcuts import render, redirect
from django.contrib import messages

from django.http import JsonResponse
from django.core.mail import send_mail
from .models import Service, PortfolioProject, InternshipProgram, ContactMessage, InternshipApplication, TeamMember, Testimonial

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ContactSerializer





@api_view(['POST'])
def contact_api(request):
    serializer = ContactSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        send_mail(
            subject=f"New Contact Form: {serializer.validated_data['subject']}",
            message=f"""
Name: {serializer.validated_data['name']}
Email: {serializer.validated_data['email']}
Phone: {serializer.validated_data.get('phone', '')}

Message:
{serializer.validated_data['message']}
""",
            from_email='nebulageotechnologies@gmail.com',
            recipient_list=['nebulageotechnologies@gmail.com'],
            fail_silently=False,
        )

        return Response({
            "status": "success",
            "message": "Contact form submitted successfully"
        })

    return Response(serializer.errors, status=400)

def home(request):
    services = Service.objects.filter(is_active=True)[:6]
    projects = PortfolioProject.objects.filter(is_featured=True)[:4]
    testimonials = Testimonial.objects.filter(is_active=True)[:4]
    stats = {
        'projects': 50,
        'clients': 30,
        'experience': 5,
        'team': 10,
    }
    return render(request, 'main/home.html', {
        'services': services,
        'projects': projects,
        'testimonials': testimonials,
        'stats': stats,
    })


def about(request):
    team = TeamMember.objects.filter(is_active=True)
    return render(request, 'main/about.html', {'team': team})


def services(request):
    services_list = Service.objects.filter(is_active=True)
    internships = InternshipProgram.objects.filter(is_active=True)
    return render(request, 'main/services.html', {
        'services': services_list,
        'internships': internships,
    })


def portfolio(request):
    category = request.GET.get('category', 'all')
    projects = PortfolioProject.objects.all()
    if category != 'all':
        projects = projects.filter(category=category)
    categories = PortfolioProject.CATEGORY_CHOICES
    return render(request, 'main/portfolio.html', {
        'projects': projects,
        'categories': categories,
        'active_category': category,
    })


def internship(request):
    programs = InternshipProgram.objects.filter(is_active=True)
    return render(
        request,
        'main/internship.html',
        {'programs': programs}
    )




def internship_apply(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        college = request.POST.get("college")
        department = request.POST.get("department")
        year = request.POST.get("year")
        internship_program = request.POST.get("internship_program")
        skills = request.POST.get("skills")
        message = request.POST.get("message")

        InternshipApplication.objects.create(
            name=name,
            email=email,
            phone=phone,
            college=college,
            department=department,
            year=year,
            internship_program=internship_program,
            skills=skills,
            message=message,
        )

        try:
            send_mail(
                subject="New Internship Application",
                message=f"""
Name: {name}
Email: {email}
Phone: {phone}
College: {college}
Department: {department}
Year: {year}
Program: {internship_program}
Skills: {skills}

Message:
{message}
""",
                from_email="nebulageotechnologies@gmail.com",
                recipient_list=["nebulageotechnologies@gmail.com"],
                fail_silently=False,
            )
        except Exception as e:
            print("MAIL ERROR:", e)

        messages.success(
            request,
            "Internship application submitted successfully."
        )

        return redirect("internship_apply")

    return render(request, "main/internship_apply.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()
        service_interested = request.POST.get("service_interested", "").strip()

        if name and email and subject and message:
            ip = request.META.get("REMOTE_ADDR")

            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
                service_interested=service_interested,
                ip_address=ip,
            )

            messages.success(
                request,
                "Thank you for reaching out! We will get back to you within 24 hours."
            )

            return redirect("contact")

        messages.error(
            request,
            "Please fill in all required fields."
        )

        return redirect("contact")

    services_list = Service.objects.filter(is_active=True)
    return render(
        request,
        'main/contact.html',
        {'services': services_list}
    )


def privacy_policy(request):
    return render(request, 'main/privacy.html')


def terms(request):
    return render(request, 'main/terms.html')
