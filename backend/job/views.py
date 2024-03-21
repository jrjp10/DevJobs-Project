from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import JobSerializer
from .models import Job
from rest_framework.exceptions import ValidationError
from django.db.models import Avg, Min, Max, Count
from account.models import CompanyProfile
# Create your views here.

#for getting all jobs
class AllJob(ListAPIView):
    """
    List all Jobs.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer


# for getting sigle job    
class JobListCreate(generics.ListCreateAPIView):
    """
    Create a new job and listi
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes =  [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def post(self, request, *args, **kwargs):
        try:
            # Get the current user's company profile
            company_profile = request.user.company_profile
        except CompanyProfile.DoesNotExists:
            return Response({"error": "User does not have a company profile."},status=status.HTTP_400_BAD_REQUEST)
        
        existing_job =  Job.objects.filter(company=company_profile, title=request.data.get('title')).first()

        if existing_job:
            raise ValidationError("You have already posted a job with the same title.")
             
        # Add the company Id to the request
        request.data['company'] = company_profile.id

        # Create a new Job instance
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data, status=status.HTTP_201_CREATED)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]  
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        obj = get_object_or_404(self.queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Manually set the companyfeild based on the authenticated user
        company_profile = request.user.company_profile
        request.data['company'] = company_profile.id

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message':'Job Deleted Successfully'},status=status.HTTP_204_NO_CONTENT)
    

class GetTopicStats(generics.RetrieveAPIView):
    def get(self, request, topic):
        args = {'title__contains': topic}
        jobs = Job.objects.filter(**args)

        if len(jobs) == 0:
            return Response({'message':f'No matching stats found for {topic}'})
        
        stats = jobs.aggregate(
            total_jobs = Count('title'),
            avg_postitions = Avg('positions'),
            avg_salary = Avg('salary'),
            max_salary = Max('salary')
        )
        return Response(stats)