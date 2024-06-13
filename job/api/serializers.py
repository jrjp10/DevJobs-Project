from rest_framework import serializers
from ..models import Job

class JobSerializer(serializers.ModelSerializer):

    """
    Serializer for the Job model.

    Validates that a job title is unique within the same company.
    """
    
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'job_type', 'education', 'it_industry', 'experience', 'salary', 'positions', 'last_date']

    def validate(self, data):
        title = data.get('title')
        company = data.get('company')
        if company:
            existing_job = Job.objects.filter(company=company, title=title).first()
            if existing_job:
                raise serializers.ValidationError("A job with this title already exists for your company.")
        return data