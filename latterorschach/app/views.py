from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Latte, Interpretation, User
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login

from .quotes import get_quote

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import logging

logger = logging.getLogger("django.views")

@csrf_exempt
@login_required
def today(request):
    latte = Latte.objects.last()
    if request.method == 'POST':
        response = request.POST.get('response')
        if request.POST.get('response') != "":
            logger.info(f"{request.user.username} said "
                        f"\"{response}\" about latte {latte.date}")
            
            interpretation = Interpretation.objects.create(user=request.user,
                                                text=response,
                                                latte=latte)
            interpretation.save()
            return redirect('topinterpretations')
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

@csrf_exempt
def account(request):
    """View function for home page of site."""
    return render(request, 'account.html')

@csrf_exempt
def history(request):
    """View function for home page of site."""
    return render(request, 'reviewHistory.html')

@csrf_exempt
def topinterpretations(request):
    latte = Latte.objects.last()
    interpretations = Interpretation.objects.all().filter(latte=latte)
    context = {
        'latte': latte,
        'interpretations': [ { "text" : interp.text, "user" : interp.user.username} for interp in interpretations]
    }
    template = loader.get_template('topInterpretations.html')
    return HttpResponse(template.render(context, request))

@csrf_exempt
def menu(request):
    """View function for home page of site."""
    if request.method == 'POST':
        logout(request)
        return redirect('/login') 
    context = {
        'quote': get_quote(),
    }
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))

@csrf_exempt
@login_required
def accountsettings(request):
    if request.method == 'POST':
        return redirect('/menu') 
    return render(request, 'accountsettings.html')

@csrf_exempt
@login_required
def changeusername(request):
    if request.method == 'POST':
        current_user = request.user
        original_username = request.POST.get('original_username')
        original_password = request.POST.get('original_password')
        new_username = request.POST.get('new_username')

        user = authenticate(username=original_username, password=original_password)
        if user is None or user != current_user:
            return HttpResponse("Invalid username or password for the current user.", status=400)
        user.username = new_username

        try:
            user.save()
        except Exception as exception:
            return HttpResponse(f"Error updating username: {str(exception)}", status=400)
        
        return redirect('/accountsettings') 
    return render(request, 'changeusername.html')

@csrf_exempt
@login_required
def changepassword(request):
    if request.method == 'POST':
        current_user = request.user
        original_username = request.POST.get('original_username')
        original_password = request.POST.get('original_password')
        new_password = request.POST.get('new_password')

        user = authenticate(username=original_username, password=original_password)
        if user is None or user != current_user:
            return HttpResponse("Invalid username or password for the current user.", status=400)
        
        if not new_password:
            return HttpResponse("New password cannot be empty.", status=400)
        
        if new_password == original_password:
            return HttpResponse("New Password shouldn't equal old password.", status=400)

        user.set_password(new_password)
        try:
            user.save()
            login(request, user)
        except Exception as exception:
            return HttpResponse(f"Error updating password: {str(exception)}", status=400)
        return redirect('/accountsettings') 
    return render(request, 'changepassword.html')

@csrf_exempt
@login_required
def changecolor(request):
    return render(request, 'changecolor.html')