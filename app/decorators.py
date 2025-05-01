from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        
        
        
        if request.session.get('user_type') == 'admin':
            return view_func(request, *args, **kwargs)


        return HttpResponseForbidden("You need to be a Admin to access this page.")
    return _wrapped_view