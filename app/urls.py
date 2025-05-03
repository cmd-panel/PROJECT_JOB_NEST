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
    # path('test-auth/', views.test_auth, name='test_auth'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('jobs/', views.browse_jobs, name='browse_jobs'),
    
    path('applications/', views.dashboard_view, name='application_list'),
    path('applications/add/<int:job_id>/', views.add_applicant_form, name='add_applicant_form'),
    path('applications/<int:pk>/update/', views.update_status, name='update_status'),
    
    path('portfolio/', views.index, name='index'),
    path('portfolio/add/', views.add_portfolio, name='portfolio_add'),         # Show add form
    path('portfolio/update/<uuid:pk>/', views.update_portfolio_view, name='portfolio_update'),
    path('portfolio/delete/<uuid:pk>/', views.delete_portfolio, name='portfolio_delete'),
    # Optional API endpoints
    path('api/add/', views.add_portfolio_api),
    path('api/update/', views.update_portfolio),
    
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/filter/', views.filter_notifications, name='filter_notifications'),
    path('notifications/delete/<int:pk>/', views.delete_notification, name='delete_notification'),
    path('notifications/toggle/<int:pk>/', views.toggle_notification_read, name='toggle_notification_read'),
    # path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),





    #nafisa
    path('update_profile/', views.update_profile, name='update_profile'),
    path('create_job/', views.create_job, name='create_job'),
    path('suggestions/', views.suggestions, name='suggestions'),
    path('chat/<str:username>/', views.chat_view, name='chat'),
    path('inbox/', views.chat_list, name='inbox'),
    path('messages_send/', views.messages_send, name='messages_send'),
    path('change_password/',views.change_password, name='change_password'),

    #wasib
    path('create_cv/', views.create_cv, name='create_cv'),
    path('applicant/', views.applicant , name='applicant'),
    
    path('compare_jobs/', views.compare_jobs, name='compare_jobs'),
    path('admin_home/', views.admin_home , name='admin_home'),
    path('admin_post_allow/', views.admin_post_allow, name='admin_post_allow'),
    path('admin_post_reject/', views.admin_post_reject, name='admin_post_reject'),

    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('admin_login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/add-videos/', views.add_course_videos, name='add_course_videos'),
    path('courses/<int:course_id>/select-video-count/', views.select_video_count, name='select_video_count'),
    


]

