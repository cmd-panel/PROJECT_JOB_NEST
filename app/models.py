from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    class Meta:
        app_label = 'app'
    def __str__(self):
        return self.user.username
    

class JobPosting(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, default=1)#DO NOT REMOVE
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    working_hours = models.IntegerField(default=0)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=50)
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    #wasib
    status = models.IntegerField(default=0)
    # posted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title} at {self.company}"
#SUZANA
class JobLocation(models.Model):
    job = models.OneToOneField(JobPosting, on_delete=models.CASCADE, related_name="geo")
    latitude = models.FloatField()
    longitude = models.FloatField()   
    
#SUZANA
#APPLICATION
from django.contrib.auth.models import User




class Application(models.Model):
    STATUS_CHOICES = [
        ('Under Review', 'Under Review'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Hired', 'Hired'),
    ]
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, null=True)#DO NOT CHANGE
    position = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')  # optional, if used
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Under Review')

    def __str__(self):
        return f"{self.applicant.username} - {self.position}"
#PORTFOLIO   
import uuid
from django.db import models
    
class Portfolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.TextField(help_text="Separate multiple links with commas")


    def __str__(self):
        return f"{self.title} - {self.user_id}"
class Certificate(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='certificates')
    image = models.ImageField(upload_to='certificates/')

    def __str__(self):
        return f"Certificate for {self.portfolio.title}"
#NOTIFICATION
class Notification(models.Model):
    TYPE_CHOICES = [
        ('Application', 'Application'),
        ('Job Update', 'Job Update'),
        ('Connection Request', 'Connection Request'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # New field
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Application')  # <<< ADD THIS LINE

    def __str__(self):
        return f"{self.user.username} - {self.title}"
    

#wasib 

class CV(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    education = models.TextField()
    experience = models.TextField()
    skills = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class UserDetails(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    skills = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='photos/', blank=True, null=True)
    
    date_of_birth = models.DateField(blank=True, null=True)
    user_type = models.CharField(max_length=100, choices=[('admin', 'Admin'), ('user', 'User'), ('premium_user', 'Premium')], default='user')

    # def __str__(self):
    #     return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from urllib.parse import urlparse, parse_qs

class CourseVideo(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    youtube_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def youtube_id(self):
        parsed_url = urlparse(self.youtube_url)
        if parsed_url.hostname in ["youtu.be"]:
            return parsed_url.path[1:]
        if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
            return parse_qs(parsed_url.query).get("v", [None])[0]
        return ""
    
#nafisa
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} → {self.receiver}: {self.content[:20]}'

#end nafisa