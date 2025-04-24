
from django.contrib import admin
from django.urls import path, include
#from app import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('register/', views.register_view, name='register'),
    path('', include('app.urls')), 
]

