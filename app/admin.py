from django.contrib import admin
from .models import JobPosting, CV, Profile, Application, Portfolio, Certificate, UserDetails, CourseVideo, Course, Message
from .models import JobLocation

admin.site.register(JobPosting)
admin.site.register(JobLocation)

#wasib
admin.site.register(CV)

admin.site.register(Profile)

admin.site.register(Application)

admin.site.register(Portfolio)

admin.site.register(Certificate)

admin.site.register(UserDetails)


admin.site.register(Course)

admin.site.register(CourseVideo)

admin.site.register(Message)