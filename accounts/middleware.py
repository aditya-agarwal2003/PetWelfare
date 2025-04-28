from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and trying to access the login page
        if request.user.is_authenticated and (request.path == reverse('login') or request.path == reverse('register')):
            return redirect('landing_page')  # Replace 'landing_page' with the name of your landing page URL

        response = self.get_response(request)
        return response