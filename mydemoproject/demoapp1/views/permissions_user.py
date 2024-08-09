from functools import wraps
from django.core.exceptions import PermissionDenied


def user_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            raise PermissionDenied("Admins cannot access this view.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
