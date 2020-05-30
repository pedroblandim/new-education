# our own custom decorators

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

def logout_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):
    """
    Decorator for views that checks that the user isn't registered, 
    redirecting to home page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: (not u.is_authenticated),
        login_url=login_url, 
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
