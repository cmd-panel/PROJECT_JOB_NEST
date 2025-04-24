
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm ,  UserLoginForm
from .models import JobPosting
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