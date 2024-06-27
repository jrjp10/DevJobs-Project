# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import generics
from django.http import HttpResponse
import zipfile
import os
from django.conf import settings
from django.contrib import messages


from .models import Application
from .serializers import ApplicationSerializer, ApplicationUpdateSerializer
from job.models import Job 
from account.api.permissions import *
from account.models import CandidateProfile
from account.models import CompanyProfile

User = get_user_model()




# Create your views here.
class ApplicationCreateAPIView(APIView):

    """
    API view for creating a job application.

    Allows authenticated candidate users to apply for a job by providing the job UUID.
    Ensures that a candidate cannot apply for the same job multiple times.
    """

    permission_classes = [IsAuthenticated,IsCandidateUser]
    authentication_classes = [JWTAuthentication]
    

    def post(self, request):
        job_uuid = request.data.get('job')

        # Check if the job post UUID is provided
        if not job_uuid:
            return Response({"message": "Please provide the job post UUID."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Get the job post instance usign uuid
        job = get_object_or_404(Job, uuid=job_uuid)

        try:
            candidate_profile = CandidateProfile.objects.get(user=request.user)

        except User.DoesNotExist:
            return Response({"message": "User not found."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        except CandidateProfile.DoesNotExist:
            return Response({"message": "Candidate profile not found."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if the candidate has already applied for this job post
        if Application.objects.filter(candidate=candidate_profile, job=job).exists():
            return Response({"message": "You have already applied for this job."},
                            status=status.HTTP_400_BAD_REQUEST)
        

        # prepare application data
        application_data = {
            'candidate' : candidate_profile.id,
            'job' : job.id
        }


        # Creating an Application instance
        serializer = ApplicationSerializer(data=application_data, context={'request':request})


        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Application submitted successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationsListAPIView(generics.ListAPIView):

    """
    API view for retrieving a list of job applications.

    Allows admin users or company users to view all job applications.
    """

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAdminUser | IsCompanyUser]
    authentication_classes = [JWTAuthentication]




class ApplicationUpdateAPIView(APIView):

    """
    API view for updating a job application.

    Allows authenticated company users to update the status of an application.
    Ensures that only the company that posted the job can update the application.
    """

    permission_classes = [IsAuthenticated ,IsCompanyUser]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, uuid):
        application = get_object_or_404(Application, uuid=uuid)

        if application.job.company.user != request.user:
            return Response({"message": "You are not authorized to update this application."},
                            status=status.HTTP_403_FORBIDDEN)
        
        serializer = ApplicationUpdateSerializer(application, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








class ApplicationDeleteAPIView(APIView):

    """
    API view for deleting a job application.
    """

    permission_classes = [IsAdminUser | IsCompanyUser]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, uuid):
        application = get_object_or_404(Application, uuid=uuid)

        # Check if the user is authorized to delete this application
        if application.job.company.user != request.user:
            return Response({"message": "You are not authorized to delete this application."},
                            status=status.HTTP_403_FORBIDDEN)
        
        application.delete()
        
        return Response({"message": "Application deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)
    


class ApplicationAPIView(APIView):

    """
    API view for retrieving , updating and deleting job application
    """

    permission_classes = [IsAuthenticated, (IsAdminUser | IsCompanyUser)]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, uuid):
        application = get_object_or_404(Application, uuid=uuid)

        if application.job.company.user != request.user:
            return Response({"message": "You are not authorized to update this application."},
                            status=status.HTTP_403_FORBIDDEN)
        
        serializer = ApplicationSerializer(application, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Status updated",
                "data": serializer.data
                }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        application = get_object_or_404(Application, uuid=uuid)

        if application.job.company.user != request.user:
            return Response({"message": "You are not authorized to delete this application."},
                            status=status.HTTP_403_FORBIDDEN)
        
        application.delete()
        return Response({"message":"Application deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)


class DownloadResumeAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            company_profile = request.user.company_profile
        except CompanyProfile.DoesNotExist:
            return Response({"message": "Company profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve all the jobs posted by the company
        jobs = Job.objects.filter(company=company_profile)

        # Create a zip file containing all resumes
        zip_filename = f"{company_profile.company_name}_resumes.zip"
        zip_file_path = os.path.join(settings.MEDIA_ROOT, zip_filename)
        
        try:
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for job in jobs:
                    applications = Application.objects.filter(job=job)
                    for application in applications:
                        candidate_profile = application.candidate
                        if candidate_profile.resume and candidate_profile.resume.name:
                            try:
                                resume_path = candidate_profile.resume.path
                                zipf.write(resume_path, os.path.basename(resume_path))
                            except ValueError as e:
                                print(f"Error: {e}")
                    
        # Prepare response to download zip file
            with open(zip_file_path, 'rb') as zipf:
                response = HttpResponse(zipf.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename={zip_filename}'

                # Optionally use Django messages framework
                messages.success(request, "Resumes downloaded successfully.")

            # Remove the zip file after sending the response
            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)

            return response
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)