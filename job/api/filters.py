from django_filters import FilterSet, ChoiceFilter, NumberFilter, CharFilter
from ..models import Job, JobType, Education, Experience

class JobFilter(FilterSet):

    """
    FilterSet for filtering job listings.
    """

    keyword = CharFilter(field_name='title', lookup_expr='icontains')
    min_salary = NumberFilter(field_name='salary', lookup_expr='gte')
    max_salary = NumberFilter(field_name='salary', lookup_expr='lte')
    education = ChoiceFilter(choices=Job._meta.get_field('education').choices)
    experience = ChoiceFilter(choices=Job._meta.get_field('experience').choices)
    job_type = ChoiceFilter(choices=Job._meta.get_field('job_type').choices)
    location = CharFilter(lookup_expr='icontains')


    class Meta:
        model = Job
        fields = {
            'job_type': ['exact'],
            'education': ['exact'],  
            'experience': ['exact'], 
            'salary': ['gte', 'lte'],
            'location': ['icontains'],
        }
        