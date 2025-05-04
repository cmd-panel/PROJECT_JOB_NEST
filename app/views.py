
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm ,  UserLoginForm
from .models import JobPosting, UserDetails, Message
from .forms import JobFilterForm
from django.db.models import Q

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from .models import Notification
from django.urls import reverse
from django.http import HttpResponseForbidden

from django.contrib.auth.decorators import login_required
from .models import PremiumSubscription
from django.contrib import messages
from django.http import HttpResponse
from .models import Connection

#wasib
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
#end wasib


#Mayami
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # handle resume saving if needed
            return redirect('login')
            
    else:
        form = UserRegistrationForm()
    return render(request, 'app/register.html', {'form': form})

def login_view(request):
    print("Login view is working...")
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Get the 'next' parameter from the URL or use a default
            print(f"User authenticated: {request.user.is_authenticated}")
            next_url = request.GET.get('next', 'browse_jobs')
            return redirect(next_url)
            # return redirect('browse_jobs')  
    else:
        form = UserLoginForm()
    return render(request, 'app/login.html', {'form': form})

# def test_auth(request):
#     if request.user.is_authenticated:
#         return HttpResponse(f"You are authenticated as {request.user.username}")
#     else:
#         return HttpResponse("You are not authenticated") 
def logout_view(request):
    logout(request)
    return redirect('login')
def home_view(request):
    return render(request, 'app/home.html')

def dashboard_view(request):
    return render(request, 'app/dashboard.html')

def browse_jobs(request):
    form = JobFilterForm(request.GET or None)
    
    #wasibjobs = JobPosting.objects.exclude(employer=request.user)
    jobs = JobPosting.objects.filter(status=1).order_by('-posted_at').exclude(employer=request.user)
    #wasib end

    if form.is_valid():
        location = form.cleaned_data.get('location')
        category = form.cleaned_data.get('category')
        experience_level = form.cleaned_data.get('experience_level')
        keyword = form.cleaned_data.get('keyword')

        if location:
            jobs = jobs.filter(location__icontains=location)
        if category:
            jobs = jobs.filter(category__icontains=category)
        if experience_level:
            jobs = jobs.filter(experience_level__icontains=experience_level)
        if keyword:
            jobs = jobs.filter(
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(company__icontains=keyword)
            )

    context = {
        'form': form,
        'jobs': jobs
    }
    return render(request, 'app/browse_jobs.html', context)
#Mayami end

#SUZANA


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Application
from .forms import StatusUpdateForm
from .forms import ApplicationForm

def add_applicant_form(request, job_id):
    job = get_object_or_404(JobPosting, pk=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.job_posting = job
            application.position = job.title
            application.status = 'Under Review'
            application.save()
            return redirect('application_list')
    else:
        form = ApplicationForm()
    return render(request, 'app/add_applicant.html', {'form': form, 'job': job})

@login_required
def dashboard_view(request):
    from_notification = request.GET.get('from_notification') == 'true'
    print("DEBUG: from_notification =", from_notification)
    if not from_notification:
        applications = Application.objects.filter(job_posting__employer=request.user)
        jobs = JobPosting.objects.filter(employer=request.user)
    else:
        applications = Application.objects.filter(applicant=request.user)
        jobs = JobPosting.objects.all() 
         
      # Only show their own jobs
    # Or maybe [] if regular users shouldn't see jobs

    return render(request, 'app/applicant_list.html', {
        'applications': applications,
        'jobs': jobs,
        'from_notification': from_notification,
    })

# @login_required
# #@csrf_protect 
# def dashboard_view(request):
    
#     if request.user.is_staff:
#         # Employer: Show only applications they postedapplications = Application.objects.filter(job_post__employer=request.user)
#         applications = Application.objects.filter(job_post__employer=request.user)
#         jobs = JobPosting.objects.all() 
        
#     else:
#         applications = Application.objects.filter(applicant=request.user)
#     return render(request, 'app/applicant_list.html', {'applications': applications, 'jobs': jobs})
@login_required
#@csrf_protect 
def update_status(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST, instance=application)
        if form.is_valid():
            updated_application = form.save()
            Notification.objects.create(
                user=updated_application.applicant,
                title="Application Status Updated",
                message=f"Your application for '{updated_application.position}' is now '{updated_application.status}'.",
                # Direct link to the specific applicationlink=reverse('application_detail', args=[updated_application.pk]),
                link=reverse('application_list')+ f"?from_notification=true",  # Adjust if you have a view for this
                type="Application"
            )
    return redirect('application_list')  # Redirect to dashboard after update
#PORTFOLIO
from .models import Portfolio, Certificate
from .forms import PortfolioForm
from django.http import JsonResponse
import json

@login_required
# Show portfolio list with update/delete forms
def index(request):
    if request.user.is_staff:
        # Employer: Show only applications they postedapplications = Application.objects.filter(job_post__employer=request.user)
        portfolios = Portfolio.objects.all()
        
    else:
        
        portfolios = Portfolio.objects.filter(user_id=request.user)
    return render(request, 'app/portfolio_list.html', {'data': portfolios})

@login_required
def add_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)  # Create the portfolio but don't save to the database yet
            portfolio.user_id = request.user  # Set the user field
            portfolio.save()  # Now save the portfolio to the database
            for file in request.FILES.getlist('certificates'):
                Certificate.objects.create(portfolio=portfolio, image=file)
            return redirect('index')  # <-- Redirect after successful POST
        else:
            print("Form is not valid:", form.errors)
    else:
        form = PortfolioForm()
    return render(request, 'app/portfolio_form.html', {'form': form})

@login_required
def update_portfolio_view(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            deleted_count = 0
            # Handle certificate deletions
            for cert in portfolio.certificates.all():
               if f'delete_cert_{cert.id}' in request.POST:
                   print(f"Deleting certificate: {cert.id}")
                   cert.delete()
                   deleted_count += 1
            if deleted_count > 0:
                messages.success(request, f"{deleted_count} certificate(s) deleted successfully!")
            form.save()
            

            for file in request.FILES.getlist('certificates'):
                Certificate.objects.create(portfolio=portfolio, image=file)
        else:
            print("Update form errors:", form.errors)
    return redirect('index')
from django.contrib import messages
def delete_portfolio(request, pk):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, pk=pk)
        portfolio.delete()
        messages.success(request, "Portfolio deleted successfully!")  
        return redirect('index')
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def add_portfolio_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            Portfolio.objects.create(
                user_id=data['user_id'],
                title=data['title'],
                description=data['description'],
                link=data['link']
            )
            return JsonResponse({"message": "Portfolio added successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST requests allowed"}, status=405)

@csrf_exempt
def update_portfolio(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            portfolio = get_object_or_404(Portfolio, id=data['id'])
            portfolio.title = data['title']
            portfolio.description = data['description']
            portfolio.link = data['link']
            portfolio.save()
            return JsonResponse({"message": "Portfolio updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST requests allowed"}, status=405)

# @csrf_exempt
# def delete_portfolio(request, pk):
#     try:
#         portfolio = get_object_or_404(Portfolio, pk=pk)
#         portfolio.delete()
#         return JsonResponse({"message": "Portfolio deleted successfully"})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=400)
#NOTIFICATION
from django.db.models import Q
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'app/notifications.html', {'notifications': notifications})

from django.db.models import Q

def filter_notifications(request):
    query = request.GET.get('q', '')
    notif_type = request.GET.get('type', '')  # <-- NEW: get type from URL

    filters = Q(user=request.user)

    if query:
        filters &= Q(title__icontains=query) | Q(message__icontains=query)

    if notif_type:
        filters &= Q(type=notif_type)  # <-- NEW: filter by type

    notifications = Notification.objects.filter(filters).order_by('-created_at')

    return render(request, 'app/notifications.html', {
        'notifications': notifications,
        'query': query,
        'notif_type': notif_type,  # pass notif_type back if you need to show selected type
    })

from django.shortcuts import redirect

def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    return redirect('notification_list')

def toggle_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.read = not notification.read
    notification.save()
    return redirect('notification_list')  # or wherever you render the list







#nafisa
from .models import UserDetails

def update_profile(request): 
    if request.method == "GET":
        return render(request, 'app/update_profile.html', {})
    elif request.method == "POST":
        profile_picture = request.FILES.get("profile_picture")
        bio = request.POST.get("bio")
        name=request.POST.get("name")
        skills = request.POST.get("skills")
        date_of_birth = request.POST.get("date_of_birth")
        location = request.POST.get("location")
        my_id = request.user
        new_obj = UserDetails.objects.filter(user_id=my_id).first()

        if new_obj:
            if profile_picture:
                new_obj.profile_picture = profile_picture
            new_obj.bio = bio
            new_obj.skills = skills
            new_obj.date_of_birth = date_of_birth
            new_obj.location = location
            new_obj.name=name
            new_obj.save()
        else:
            new_obj = UserDetails.objects.create(
                user_id=my_id,
                profile_picture=profile_picture if profile_picture else None,
                bio=bio,
                skills=skills,
                date_of_birth=date_of_birth,
                location=location,
                name=name
            )

        return redirect('browse_jobs')  

    return render(request, 'app/update_profile.html', {})
# @login_required
# def update_profile(request):
#     
#         print("DEBUG: GET request received.")
#         

#         return render(request, 'app/update_profile.html', {})

#     
#         print("DEBUG: POST request received.")

#         profile, created = UserDetails.objects.get_or_create(user_id=request.user)
#         if created:
#             print(f"DEBUG: Created new UserDetails for user {request.user.username} (ID: {request.user.id})")
#         else:
#             print(f"DEBUG: Found existing UserDetails for user {request.user.username} (ID: {request.user.id})")

#         if request.FILES.get("profile_picture"):
#             profile.profile_picture = request.FILES["profile_picture"]
#             print("DEBUG: Profile picture updated.")

#         if request.POST.get("bio"):
#             profile.bio = request.POST["bio"]
#             print("DEBUG: Bio updated.")

#         if request.POST.get("skills"):
#             profile.skills = request.POST["skills"]
#             print("DEBUG: Skills updated.")

#         if request.POST.get("location"):
#             profile.location = request.POST["location"]
#             print("DEBUG: Location updated.")

#         if request.POST.get("date_of_birth"):
#             profile.date_of_birth = request.POST["date_of_birth"]
#             print("DEBUG: Date of birth updated.")

#         profile.save()
#         print("DEBUG: Profile successfully saved.")
#         return redirect('update_profile')



#         # profile_picture= request.POST.get("profile_picture")

#         # bio= request.POST.get("bio")

#         # skills= request.POST.get("skills")

#         # date_of_birth= request.POST.get("date_of_birth")

#         location= request.POST.get("location")
#         

        
        # # my_id= request.user.id new_obj= UserDetails.objects.filter()id=my_id
        # new_obj=UserDetails.objects.filter(user_id=request.user)

        # new_obj.update(profile_picture=profile_picture, bio=bio, skills= skills, date_of_birth=date_of_birth)
        


@login_required
def create_job(request):
    if request.method == "GET":
        return render(request, 'app/create_job.html', {})
    elif request.method == "POST":
        title= request.POST.get("title")

        company= request.POST.get("company")
        
        salary = request.POST.get("salary")
        
        working_hours = request.POST.get("working_hours")

        location= request.POST.get("location", "").strip()

        category= request.POST.get("category")

        experience= request.POST.get("experience")

        job=JobPosting.objects.create(title=title, salary=salary, working_hours=working_hours,company=company, location=location, category=category, experience_level=experience, employer=request.user)
        #SUZANA
        

        matching_users = UserDetails.objects.filter(skills__icontains=category).exclude(user_id=job.employer)

        for user_detail in matching_users:
            Notification.objects.create(
                user=user_detail.user_id,
                title="New Job Alert",
                message=f"A new job '{title}' matching your skills has been posted.",
                link=reverse('browse_jobs'),
                type='Job Update'
            )
        # Get geo coordinates
        lat, lng = geocode_location(location)
        if lat and lng:
            JobLocation.objects.create(job=job, latitude=lat, longitude=lng)
        return redirect ('browse_jobs')

    return redirect('create_job')
#SUZANA
def compare_jobs(request):
    jobs = JobPosting.objects.all().select_related('geo')
    sort_by = request.GET.get("sort")
    min_hours = request.GET.get("min_hours")
    max_hours = request.GET.get("max_hours")

    if min_hours:
        jobs = jobs.filter(working_hours__gte=int(min_hours))
    if max_hours:
        jobs = jobs.filter(working_hours__lte=int(max_hours))

    if sort_by == "salary":
        jobs = jobs.order_by("-salary")
    elif sort_by == "hours":
        jobs = jobs.order_by("working_hours")

    return render(request, 'app/compare_jobs.html', {'jobs': jobs, 'mapbox_token': MAPBOX_ACCESS_TOKEN})

import requests
from .models import JobPosting, JobLocation

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1Ijoic3N1emFuYTQ0IiwiYSI6ImNtYTJxMDM4ajI5azcybHBwNHd1d2tsbnYifQ.UH_K-8ytJKiyU6OHtOvAkw'

def geocode_location(location):
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json"
    params = {"access_token": MAPBOX_ACCESS_TOKEN}
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200 and data["features"]:
        longitude, latitude = data["features"][0]["center"]
        return longitude,latitude
    return None, None


@login_required
def suggestions(request):
    if request.method == "GET":
        
        my_id = request.user
        temp = UserDetails.objects.get(user_id=my_id)
        temp_location = temp.location
        temp_skills = temp.skills
        
        
        user_list = UserDetails.objects.filter(Q(location__icontains=temp_location) | Q(skills__icontains=temp_skills)).order_by('-created_at')
        data={
            'user_list': user_list,
            
        }

        return render(request, 'app/suggestions.html', data)
            
    my_id = request.user
    temp = UserDetails.objects.get(user_id=my_id)
    temp_location = temp.location
    temp_skills = temp.skills
    
        
    user_list = UserDetails.objects.filter(Q(location__icontains=temp_location) | Q(skills__icontains=temp_skills)).order_by('-created_at')
    data={
            'user_list': user_list,
            
        }

    return render(request, 'app/suggestions.html', data)



#wasib
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import CV, Course, CourseVideo
from .forms import CVForm, ApplicationForm1, CourseForm, CourseVideoForm
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.forms import modelformset_factory




@login_required
def create_cv(request):
    if request.method == 'POST':
        form = CVForm(request.POST)
        if form.is_valid():
            cv = form.save()

            # Generate PDF
            template = get_template('app/cv_template.html')
            html = template.render({'cv': cv})
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{cv.name}_cv.pdf"'

            pisa_status = pisa.CreatePDF(html, dest=response)

            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    else:
        form = CVForm()

    return render(request, 'app/cv_form.html', {'form': form})


from .forms import ApplicationForm1
@login_required
def applicant(request):
    if request.method == 'POST':
        form = ApplicationForm1(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.save()
            return redirect('browse_jobs')  # Redirect to the same page after saving
    
    form = ApplicationForm1()
    
    
    return render(request, 'app/applicant.html', {'form': form})



@login_required
@admin_required
def admin_home(request):
    if request.method == "GET":
        # Fetch all job posts from the database
        
        job_posts = JobPosting.objects.filter(status=0).order_by('-posted_at')
        data={
            'job_lists': job_posts,
            
        }

        return render(request, 'app/admin_home.html', data)
    job_posts = JobPosting.objects.filter(status=0).order_by('-posted_at')
    data={
            'job_lists': job_posts,
            
        }

    return render(request, 'app/admin_home.html', data)

@login_required
@admin_required
def admin_post_allow(request):
    if request.method == "GET":
        return redirect('admin_home')
    elif request.method == "POST":
        job_id = request.POST.get('job_id')
        job_post = JobPosting.objects.get(id=job_id)
        job_post.status = 1
        job_post.save()
        return redirect('admin_home')  
    return redirect('admin_home')  


@login_required
@admin_required
def admin_post_reject(request):
    if request.method == "GET":
        return redirect('admin_home')
    elif request.method == "POST":
        job_id = request.POST.get('job_id')
        job_post = JobPosting.objects.get(id=job_id)
        job_post.delete()  
        return redirect('admin_home')  
    return redirect('admin_home')


@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'app/course_list.html', {'courses': courses})


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'app/course_detail.html', {'course': course})

def admin_login_view(request):
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            my_user=request.user
            my_details=UserDetails.objects.get(user_id=my_user)
            if my_details:
                type=my_details.user_type
                if type=='admin':
                    request.session['user_type'] = 'admin'
                    return redirect('admin_home')
                else:
                    return redirect('browse_jobs')
            else:
                return redirect('browse_jobs')
    
    else:
        form = UserLoginForm()
    return render(request, 'app/admin_login.html', {'form': form})








@login_required
@admin_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            
            return redirect('select_video_count', course_id=course.id)

    else:
        form = CourseForm()
    return render(request, 'app/add_course.html', {'form': form})


@login_required
@admin_required
def add_course_videos(request, course_id):
    course = Course.objects.get(id=course_id)

    count = int(request.GET.get('count', 2))  
    VideoFormSet = modelformset_factory(CourseVideo, form=CourseVideoForm, extra=count)

    if request.method == 'POST':
        formset = VideoFormSet(request.POST, queryset=CourseVideo.objects.none())
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    video = form.save(commit=False)
                    video.course = course
                    video.save()
            return redirect('course_detail', course_id=course.id)
    else:
        formset = VideoFormSet(queryset=CourseVideo.objects.none())

    return render(request, 'app/add_course_with_videos.html', {'formset': formset, 'course': course})



from django.urls import reverse
from django.http import HttpResponseRedirect

@login_required
@admin_required
def select_video_count(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        try:
            num_videos = int(request.POST.get('num_videos', 1))
            url = reverse('add_course_videos', args=[course_id])
            return HttpResponseRedirect(f"{url}?count={num_videos}")
        except ValueError:
            pass  # optional: add a message or error

    return render(request, 'app/select_video_count.html', {'course': course})



###wasib end


#nafisa

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
import requests
from django.core.paginator import Paginator

@login_required
def chat_view(request, username):
    user2 = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=user2) |
        Q(sender=user2, receiver=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=user2, content=content)

    return render(request, 'app/chat.html', {
        'messages': messages,
        'user2': user2,
    })

@login_required
def chat_list(request):
    
    messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    users = set()
    for msg in messages:
        if msg.sender != request.user:
            users.add(msg.sender)
        if msg.receiver != request.user:
            users.add(msg.receiver)
    return render(request, 'app/chat_list.html', {'users': users})

@login_required
def messages_send(request):
    if request.method == "GET":
        return redirect('browse_jobs')
    elif request.method == "POST":
        user_id = request.POST.get('user_id')
        my_id = request.user.id
        receiver=User.objects.get(id=user_id)
        sender=request.user
        content= request.POST.get('content')
        new_obj=Message.objects.create(sender=sender, receiver=receiver, content=content)
        new_obj.save()
        return redirect('inbox')
    return redirect('browse_jobs')


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change_password')
        

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('change_password')

        request.user.set_password(new_password)
        request.user.save()

        # Prevent user from being logged out after password change
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Password changed successfully.')
        return redirect('browse_jobs')  # Or wherever you want to go after success

    return render(request, 'app/change_password.html')



#end nafisa



##Payment_Mayami##

@login_required
def benefits_view(request):
    return render(request, 'app/benefits.html')

# @login_required
# def process_payment(request):
#     if request.method == 'POST':
#         plan = request.POST.get('plan')
#         amount = request.POST.get('amount')
#         bkash_number = request.POST.get('bkash_number')

#         # process/store the payment info here
#         print(f"Received Payment - Plan: {plan}, Amount: {amount}, bKash Number: {bkash_number}")

#         return redirect('browse_jobs')  
#     return HttpResponse("Invalid request.")
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

@login_required
def process_payment(request):
    plan = request.POST.get('plan')
    amount = request.POST.get('amount')
    bkash_number = request.POST.get('bkash_number')

    # Validate inputs
    if not plan or not amount or not bkash_number or len(bkash_number) != 11 or not bkash_number.isdigit():
        messages.error(request, "Invalid input. Please try again.")
        return redirect('benefits') 

    
    #Payment.objects.create(user=request.user, plan=plan, amount=amount, bkash_number=bkash_number) #database update

 
    request.session['payment_success'] = True

    return redirect('browse_jobs') 



# #Connection
# @login_required
# def send_request(request, user_id):
#     receiver = get_object_or_404(User, id=user_id)
#     if request.user != receiver:
#         Connection.objects.get_or_create(sender=request.user, receiver=receiver)
#     return redirect('view_users')

# @login_required
# def accept_request(request, request_id):
#     connection = get_object_or_404(Connection, id=request_id, receiver=request.user)
#     connection.is_accepted = True
#     connection.save()
#     return redirect('connection_requests')

# @login_required
# def connection_requests(request):
#     requests = Connection.objects.filter(receiver=request.user, is_accepted=False)
#     return render(request, 'connections/requests.html', {'requests': requests})

# @login_required
# def view_users(request):
#     users = User.objects.exclude(id=request.user.id)
#     sent_requests = Connection.objects.filter(sender=request.user)
#     received_requests = Connection.objects.filter(receiver=request.user)
#     connections = Connection.objects.filter(
#         models.Q(sender=request.user) | models.Q(receiver=request.user),
#         is_accepted=True
#     )
#     context = {
#         'users': users,
#         'sent_requests': sent_requests,
#         'received_requests': received_requests,
#         'connections': connections
#     }
#     return render(request, 'connections/users.html', context)

# from django.db.models import Q

# @login_required
# def my_connections(request):
#     connections = Connection.objects.filter(
#         Q(sender=request.user) | Q(receiver=request.user),
#         is_accepted=True
#     )
#     return render(request, 'app/my_connections.html', {'connections': connections})

# #Mayami end