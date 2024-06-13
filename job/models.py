from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
import uuid

from account.models import CompanyProfile
# Create your models here.

class JobType(models.TextChoices):
    FULL_TIME = 'Full Time'
    PART_TIME = 'Part Time'
    INTERNSHIP = 'Internship'

class Education(models.TextChoices):
    HIGHER_SECONDARY = 'Higher Secondary'
    BACHELORS = 'Bachelors'
    MASTER = 'Master'
    PHD = 'Phd'

class Experience(models.TextChoices):
    NO_EXPERIENCE = 'Fresher'
    ONE_YEAR = '1 Year'
    TWO_YEARS = '2 Years'
    THREE_YEARS_PLUS = '3 Years above'
    
def return_date_time():
    now = datetime.now()
    return now + timedelta(days=10)

class ITIndustry(models.TextChoices):
    SOFTWARE_DEVELOPER = 'Software Developer'
    WEB_DEVELOPER = 'Web Developer'
    MOBILE_APP_DEVELOPER = 'Mobile App Developer'
    GAME_DEVELOPER = 'Game Developer'
    EMBEDDED_SYSTEMS_DEVELOPER = 'Embedded Systems Developer'
    DEVOPS_ENGINEER = 'DevOps Engineer'
    QUALITY_ASSURANCE_ENGINEER = 'Quality Assurance Engineer'
    TEST_AUTOMATION_ENGINEER = 'Test Automation Engineer'
    FRONTEND_DEVELOPER = 'Frontend Developer'
    BACKEND_DEVELOPER = 'Backend Developer'
    FULL_STACK_DEVELOPER = 'Full Stack Developer'
    DATABASE_DEVELOPER = 'Database Developer'
    CLOUD_ENGINEER = 'Cloud Engineer'
    SYSTEMS_ENGINEER = 'Systems Engineer'
    UI_UX_DESIGNER = 'UI/UX Designer'
    SOFTWARE_ARCHITECT = 'Software Architect'
    MACHINE_LEARNING_ENGINEER = 'Machine Learning Engineer'
    AI_DEVELOPER = 'AI Developer'
    ROBOTICS_ENGINEER = 'Robotics Engineer'
    BLOCKCHAIN_DEVELOPER = 'Blockchain Developer'
    AR_VR_DEVELOPER = 'AR/VR Developer'
    IOT_DEVELOPER = 'IoT Developer'
    FIRMWARE_ENGINEER = 'Firmware Engineer'
    SECURITY_ENGINEER = 'Security Engineer'
    ETL_DEVELOPER = 'ETL Developer'
    BUSINESS_INTELLIGENCE_DEVELOPER = 'BI Developer'
    NATURAL_LANGUAGE_PROCESSING_ENGINEER = 'NLP Engineer'
    DATA_SCIENTIST = 'Data Scientist'
    DATA_ANALYST = 'Data Analyst'
    BIG_DATA_ENGINEER = 'Big Data Engineer'
    DATA_ARCHITECT = 'Data Architect'
    STATISTICAL_ANALYST = 'Statistical Analyst'
    PREDICTIVE_MODELER = 'Predictive Modeling Analyst'
    DEEP_LEARNING_ENGINEER = 'Deep Learning Engineer'
    COMPUTER_VISION_ENGINEER = 'Computer Vision Engineer'
    QUANTITATIVE_ANALYST = 'Quantitative Analyst'
    OPERATIONS_VISUALIZATION_ENGINEER = 'Data Visualization Engineer'
    RESEARCH_SCIENTIST = 'Research Scientist (Data Science)'
    DATA_MINING_ENGINEER = 'Data Mining Engineer'
    COMPUTATIONAL_LINGUIST = 'Computational Linguist'
    ANALYTICS_ENGINEER = 'Analytics Engineer'



class Job(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    location = models.CharField(max_length=100, null=True)
    job_type = models.CharField(
        max_length=10,
        choices=JobType.choices,
        default=JobType.FULL_TIME
    )
    education = models.CharField(
        max_length=20,
        choices=Education.choices,
        default=Education.BACHELORS
    )
    it_industry = models.CharField(
        max_length=40,
        choices=ITIndustry.choices,
        default=ITIndustry.FRONTEND_DEVELOPER
    )
    experience = models.CharField(
        max_length=20,
        choices=Experience.choices,
        default=Experience.NO_EXPERIENCE
    )
    salary = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(1000000)])
    positions = models.IntegerField(default=1)
    last_date = models.DateTimeField(default=return_date_time)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # # New fields for storing slugified version of job title
    # title_slug = models.SlugField(unique=True, max_length=255,default='')

    # def save(self, *args, **kwargs):
    #     # Generate slug for the job title
    #     self.title_slug = slugify(self.title)
    #     super().save(*args,**kwargs) 

    def __str__(self):
        return self.title
    
    @property
    def id(self):
        return self.uuid