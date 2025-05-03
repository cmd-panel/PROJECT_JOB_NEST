from django.contrib import admin
from django.urls import path
from . import views

#wasib
from django.conf import settings
from django.conf.urls.static import static
#wasib

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.home_view, name='home'),  
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('jobs/', views.browse_jobs, name='browse_jobs'),
    path('applications/', views.dashboard_view, name='application_list'),
    path('applications/add/', views.add_applicant_form, name='add_applicant_form'),
    path('applications/<int:pk>/update/', views.update_status, name='update_status'),
    path('portfolio/', views.index, name='index'),
    path('portfolio/add/', views.add_portfolio, name='portfolio_add'),         # Show add form
    path('portfolio/update/<uuid:pk>/', views.update_portfolio_view, name='portfolio_update'),
    path('portfolio/delete/<uuid:pk>/', views.delete_portfolio, name='portfolio_delete'),
    # Optional API endpoints
    path('api/add/', views.add_portfolio_api),
    path('api/update/', views.update_portfolio),
    path('benefits/', views.benefits_view, name='benefits'),
    path('process_payment/', views.process_payment, name='process_payment'),
    # path('users/', views.view_users, name='view_users'),
    # path('send-request/<int:user_id>/', views.send_request, name='send_request'),
    # path('accept-request/<int:request_id>/', views.accept_request, name='accept_request'),
    # path('requests/', views.connection_requests, name='connection_requests'),
    # path('my-connections/', views.my_connections, name='my_connections'),

]

