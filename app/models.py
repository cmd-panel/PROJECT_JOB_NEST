from django.db import models
from django.contrib.auth.models import User

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