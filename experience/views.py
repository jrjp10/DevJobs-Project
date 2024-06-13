from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Experience
from .serializer import ExperienceSerializer
from account.api.permissions import IsCandidateUser
from account.models import CandidateProfile
# Create your views here.

class ExperienceListAPIView(APIView):

    """
    API view to list and create experiences for a candidate user.

    This view allows authenticated candidate users to list their experiences and create new experiences.
    """
     
    permission_classes = [IsAuthenticated, IsCandidateUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        candidate_profile = CandidateProfile.objects.get(user=request.user)
        experiences = Experience.objects.filter(candidate=candidate_profile)
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExperienceDetailsAPIView(APIView):

    """
    API view to retrieve, update, and delete a specific experience for a candidate user.

    This view allows authenticated candidate users to perform CRUD operations on their experiences.
    """

    permission_classes = [IsAuthenticated, IsCandidateUser]
    authentication_classes = [JWTAuthentication]

    def get_object(self, uuid):

        """
        Get the Experience instance with the given UUID belonging to the authenticated user.

        Args:
            uuid (str): UUID of the experience.

        Returns:
            Experience: Experience instance.
        """

        candidate_profile = self.request.user.candidate_profile

        # Retrive the experience objects with the given uuid belonging to candidate_profile
        experience = get_object_or_404(Experience, uuid=uuid, candidate=candidate_profile)
        return experience
    

    def get(self, request , uuid):

        """
        Retrieve a specific experience.

        Args:
            request: HTTP request object.
            uuid (str): UUID of the experience.

        Returns:
            Response: HTTP response.
        """

        experience = self.get_object(uuid)
        serializer = ExperienceSerializer(experience, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, uuid):

        """
        Update a specific experience.

        Args:
            request: HTTP request object.
            uuid (str): UUID of the experience.

        Returns:
            Response: HTTP response.
        """
           
        experience = self.get_object(uuid)
        serializer = ExperienceSerializer(experience, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Experience updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request , uuid):

        """
        Delete a specific experience.

        Args:
            request: HTTP request object.
            uuid (str): UUID of the experience.

        Returns:
            Response: HTTP response.
        """
        
        experience = self.get_object(uuid)
        experience.delete()
        return Response({'message': 'Experience deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
