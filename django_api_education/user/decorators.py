from functools import wraps
from django.http import JsonResponse

def login_required_with_error_message(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Login is required"}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapped_view