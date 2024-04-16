from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Latte, Interpretation
from django.contrib import messages

import logging

logger = logging.getLogger("django.views")

def today(request):
  latte = Latte.objects.last()
  template = loader.get_template('dailyReview.html')
  context = {
    'latte': latte,
  }
  return HttpResponse(template.render(context, request))

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.save()
        return redirect('login')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')  # Adjust the redirect as necessary
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def account(request):
    """View function for home page of site."""
    return render(request, 'account.html')

def history(request):
    """View function for home page of site."""
    return render(request, 'reviewHistory.html')
    
def topinterpretations(request):
    """View function for home page of site."""
    return render(request, 'topInterpretations.html')

def menu(request):
    """View function for home page of site."""
    return render(request, 'home.html')
