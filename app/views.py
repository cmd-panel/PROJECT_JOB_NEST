
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm ,  UserLoginForm
from .models import JobPosting, UserDetails
from .forms import JobFilterForm
from django.db.models import Q

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
            return redirect('browse_jobs')  
    else:
        form = UserLoginForm()
    return render(request, 'app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
def home_view(request):
    return render(request, 'app/home.html')

def dashboard_view(request):
    return render(request, 'app/dashboard.html')

def browse_jobs(request):
    form = JobFilterForm(request.GET or None)
    jobs = JobPosting.objects.all()

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
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Application
from .forms import StatusUpdateForm
from .forms import ApplicationForm

def add_applicant_form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.status = 'Under Review'  # Always set
            application.save()
            return redirect('application_list')  # Use correct URL name
    else:
        form = ApplicationForm()
    return render(request, 'app/add_applicant.html', {'form': form})

@login_required
def dashboard_view(request):
    applications = Application.objects.all()
    return render(request, 'app/applicant_list.html', {'applications': applications})
@login_required
def update_status(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
    return redirect('application_list')  # Redirect to dashboard after update

from .models import Portfolio, Certificate
from .forms import PortfolioForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Show portfolio list with update/delete forms
def index(request):
    portfolios = Portfolio.objects.all()
    return render(request, 'app/portfolio_list.html', {'data': portfolios})

def add_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save()
            for file in request.FILES.getlist('certificates'):
                Certificate.objects.create(portfolio=portfolio, image=file)
            return redirect('index')  # <-- Redirect after successful POST
        else:
            print("Form is not valid:", form.errors)
    else:
        form = PortfolioForm()
    return render(request, 'app/portfolio_form.html', {'form': form})


def update_portfolio_view(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            form.save()
            for file in request.FILES.getlist('certificates'):
                Certificate.objects.create(portfolio=portfolio, image=file)
        else:
            print("Update form errors:", form.errors)
    return redirect('index')


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

@csrf_exempt
def delete_portfolio(request, pk):
    try:
        portfolio = get_object_or_404(Portfolio, pk=pk)
        portfolio.delete()
        return JsonResponse({"message": "Portfolio deleted successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    





#nafisa

def update_profile(request):
    if request.method == "GET":
        return render(request, 'update_profile.html', {})
    
    elif request.method == "POST":
        profile_picture= request.POST.get("profile_picture")

        bio= request.POST.get("bio")

        skills= request.POST.get("skills")

        date_of_birth= request.POST.get("date_of_birth")

        location= request.POST.get("location")

        my_id= request.user.id
        new_obj= UserDetails.objects.filter(user_id=my_id)
        new_obj.update(profile_picture=profile_picture, bio=bio, skills= skills, date_of_birth=date_of_birth, location=location)
        
        redirect ('browse_jobs')

def create_job(request):
    if request.method == "GET":
        return render(request, 'create_job.html', {})
    
    elif request.method == "POST":
        title= request.POST.get("title")

        company= request.POST.get("company")

        location= request.POST.get("location")

        category= request.POST.get("category")

        experience= request.POST.get("experience")

        JobPosting.objects.create(title=title, company=company, location=location, category=category, experience_level=experience)
        
        redirect ('home')

    redirect('create_job')




#wasib
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import CV
from .forms import CVForm
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
import os
from django.conf import settings
from django.contrib.staticfiles import finders





def create_cv(request):
    if request.method == 'POST':
        form = CVForm(request.POST)
        if form.is_valid():
            cv = form.save()

            # Generate PDF
            template = get_template('cv_template.html')
            html = template.render({'cv': cv})
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{cv.name}_cv.pdf"'

            pisa_status = pisa.CreatePDF(html, dest=response)

            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    else:
        form = CVForm()

    return render(request, 'cv_form.html', {'form': form})



def applicant(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            applicant = form.save()
            return redirect('browse_jobs')  # Redirect to the same page after saving
    else:
        form = ApplicationForm()
    id = request.user.id
    
    return render(request, 'applicant.html', {'form': form, 'id':id})
###wasib end


