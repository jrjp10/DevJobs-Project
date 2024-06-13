from django.contrib import admin
from .models import User, CandidateProfile, CompanyProfile

# Register your models here.
admin.site.register(User)


class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'birthday', 'location', 'skills', 'experience', 'education', 'resume', 'candidate_image']
    search_fields = ['user__email', 'name', 'location']
    ordering = ['name']

admin.site.register(CandidateProfile, CandidateProfileAdmin)


class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'industry', 'location', 'website', 'company_image']
    search_fields = ['user__email', 'company_name', 'industry', 'location']
    ordering = ['company_name']
    
admin.site.register(CompanyProfile, CompanyProfileAdmin)
