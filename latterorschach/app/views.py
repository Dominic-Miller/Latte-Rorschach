from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Latte, Interpretation

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
    """View function for home page of site."""
    return render(request, 'register.html')

def login(request):
    """View function for home page of site."""
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