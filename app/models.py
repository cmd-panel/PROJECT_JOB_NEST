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
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=50)
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"



class Application(models.Model):
    STATUS_CHOICES = [
        ('Under Review', 'Under Review'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
    ]
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')  # optional, if used
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Under Review')

    def __str__(self):
        return f"{self.applicant.username} - {self.position}"
    


class Portfolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100)
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
    bio = models.TextField()
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='photos/', blank=True, null=True)
    
    date_of_birth = models.DateField(blank=True, null=True)
    user_type = models.CharField(max_length=100, choices=[('admin', 'Admin'), ('user', 'User'), ('premium_user', 'Premium')], default='user')

    def __str__(self):
        return self.name
