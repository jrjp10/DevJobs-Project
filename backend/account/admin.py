from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import User, CandidateProfile, CompanyProfile

# Register your models here.
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'birthday', 'location', 'skills', 'experience', 'education']
    search_fields = ['user__email', 'name', 'location']
    ordering = ['name']

admin.site.register(CandidateProfile, CandidateProfileAdmin)

class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'industry', 'location', 'website']
    search_fields = ['user__email', 'company_name', 'industry', 'location']
    ordering = ['company_name']

admin.site.register(CompanyProfile, CompanyProfileAdmin)

admin.site.register(User)