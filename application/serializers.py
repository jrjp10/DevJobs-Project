from rest_framework import serializers
from .models import Application
from account.models import CandidateProfile
from job.models import Job

class ApplicationSerializer(serializers.ModelSerializer):

    """
    Serializer for the Application model.

    This serializer includes fields for displaying the candidate's name and the job title
    instead of their UUIDs.
    """

    candidate_name = serializers.CharField(source='candidate.name')
    job_title = serializers.CharField(source='job.title')
    company_name = serializers.CharField(source='job.company')

    class Meta:
        model = Application
        fields = ['uuid', 'candidate_name', 'job_title', 'company_name', 'application_date', 'status']

    
    def validate(self, attrs):

        """
        Custom validation method to ensure the uniqueness of applications.

        Checks if an application already exists for the given candidate and job combination.
        """

        candidate = attrs.get('candidate')
        job = attrs.get('job')
        if Application.objects.filter(candidate=candidate, job=job).exists():
            raise serializers.ValidationError({'error': 'Application already exists.'})
        return attrs
    

class ApplicationUpdateSerializer(serializers.ModelSerializer):

    """
    Serializer for updating an Application instance.

    This serializer allows updating all fields of the Application model.
    """
    

    company_name = serializers.CharField(source='job.company.name', read_only=True)
    
    class Meta:
        model = Application
        fields = '__all__'

