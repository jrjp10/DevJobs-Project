from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from django.db.models import Avg, Min, Max, Count
from django.utils.text import slugify
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from django.core.cache import cache
from django.conf import settings

from .serializers import JobSerializer
from ..models import Job
from account.models import CompanyProfile
from account.models import User
from .filters import JobFilter
from .pagination import CustomPagination


class CreateJob(APIView):

    """
    API view for creating and retrieving jobs.

    Allows authenticated company users to create and retrieve jobs posted by their company.

    GET: Retrieve all jobs posted by the authenticated company user.
    POST: Create a new job post for the authenticated company user.

    Requires authentication and company user role.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get(self, request):
        # company users can only access this endpoint
        if request.user.role != User.COMPANY:
            raise PermissionDenied(
                "Only company users are allowed to access this endpoint.")

        jobs = Job.objects.filter(company=self.get_company_profile())
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)




    def post(self, request):
        company_profile = self.get_company_profile()

        if not company_profile:
            return Response({"error": "User does not have a company profile."}, status=status.HTTP_400_BAD_REQUEST)


        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['company'] = company_profile
            serializer.save()
            return Response({"message": "Successfully created Jobpost"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Helper method to get the company profile of the authenticated user
    def get_company_profile(self):
        return getattr(self.request.user, 'company_profile', None)


# For Retriving , updating , deleting  a particular job
class JobRetrieveUpdateDestroy(APIView):

    """
    API view for retrieving, updating, and deleting a specific job post.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, uuid):
        return get_object_or_404(Job, uuid=uuid)


    def get(self, request, uuid):
        job = self.get_object(uuid)
        serializer = JobSerializer(job)
        return Response(serializer.data)



    def put(self, request, uuid):
        job = self.get_object(uuid)
        company_profile = self.get_company_profile()

        if not company_profile:
            return Response({"error": "User does not have a company profile."}, status=status.HTTP_400_BAD_REQUEST)


        serializer = JobSerializer(job, data=request.data, context={
                                   'company_profile': company_profile})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Job Updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, uuid):
        job = self.get_object(uuid)
        job.delete()
        return Response({"message": "Job Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


    # company = request.user.company_profile - helper
    def get_company_profile(self):
        return getattr(self.request.user, 'company_profile', None)




class AllJob(generics.ListAPIView):

    """
    API view for retrieving all jobs.
    Allows all users to retrieve a list of all job posts.
    Requires authentication.
    Supports search and filtering by various fields.
    """

    serializer_class = JobSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = JobFilter
    search_fields = ['title','location', 'job_type', 'education', 'it_industry', 'company__company_name']  # Adjusted search_fields

    def get_queryset(self):
        queryset = cache.get('all_jobs_queryset')
        if not queryset:
            queryset = Job.objects.all()
            cache.set('all_jobs_queryset', queryset, timeout=settings.CACHE_TTL)
        return queryset
