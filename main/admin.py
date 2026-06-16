from django.contrib import admin
from django.utils.html import format_html
from .models import Service, PortfolioProject, InternshipProgram, ContactMessage, TeamMember, Testimonial
from .models import InternshipApplication


admin.site.register(InternshipApplication)
admin.site.site_header = "Nebula Geo Technologies Admin"
admin.site.site_title = "Nebula Geo Admin"
admin.site.index_title = "Welcome to Nebula Geo Technologies Dashboard"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    ordering = ['order']


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'order', 'created_at']
    list_editable = ['is_featured', 'order']
    list_filter = ['category', 'is_featured']
    search_fields = ['title', 'description', 'tech_stack']
    ordering = ['order']


@admin.register(InternshipProgram)
class InternshipProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'stipend', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['title', 'description']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'service_interested', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['status']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'service_interested', 'created_at', 'ip_address']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'designation']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_company', 'rating', 'is_active', 'created_at']
    list_editable = ['is_active']
    list_filter = ['rating', 'is_active']
