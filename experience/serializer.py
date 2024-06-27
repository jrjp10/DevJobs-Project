from rest_framework import serializers
from .models import Experience

class ExperienceSerializer(serializers.ModelSerializer):

    """
    Serializer for the Experience model.

    This serializer handles the serialization and deserialization of Experience objects.
    It excludes the 'candidate' field from the serialization as it's automatically associated
    with the authenticated user (candidate).
    """

    class Meta:
        model = Experience
        exclude = ['candidate']

    def validate(self, attrs):

        """
        Validate the data for an Experience instance.
        This method checks if the end date is not before the start date.
        Args:
            attrs (dict): Dictionary containing the validated data.
        Returns:
            dict: Validated data.
        Raises:
            serializers.ValidationError: If the end date is before the start date.
        """
         
        if attrs.get('end_date') and attrs['end_date'] < attrs['start_date']:
            raise serializers.ValidationError('End date cannot be before start date')
        return attrs
    
    def create(self, validate_data):

        """
        create Experience instance.
        This method associates the authenticated user (candidate) with the experience instance
        before saving it. If an instance is provided, it updates it; otherwise, it creates a new one.
        Args:
            kwargs: Additional keyword arguments.
        Returns:
            Experience: Saved or updated Experience instance.
        """

        # Associate the authenticated user (candidate) with the experience
        candidate_profile = self.context['request'].user.candidate_profile
        validate_data['candidate'] = candidate_profile
        return super().create(validate_data)
    


