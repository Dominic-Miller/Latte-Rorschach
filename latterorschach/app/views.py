from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Latte, Interpretation, User
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login

from django.views.decorators.csrf import csrf_exempt

import logging

logger = logging.getLogger("django.views")

def today(request):
  logger.info(f"{request.user.username} logged in")
  latte = Latte.objects.last()
  template = loader.get_template('dailyReview.html')
  context = {
    'latte': latte,
  }
  return HttpResponse(template.render(context, request))

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.save()
        return redirect('login')
    return render(request, 'register.html')

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info(f"{user.username} logged in")
            return redirect('/')  # Adjust the redirect as necessary
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
