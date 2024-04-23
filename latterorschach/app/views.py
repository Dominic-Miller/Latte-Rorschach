from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Latte, Interpretation, User, Like
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.http import QueryDict
from .quotes import get_quote
from datetime import datetime, timedelta

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
            return redirect('/')
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
    interpretations = Interpretation.objects.all().filter(user=request.user)

    t_likes = 0
    t_interps = 0

    interps_list = []
    for interp in interpretations:
        likes = len(Like.objects.all().filter(interpretation=interp))

        t_likes += likes
        t_interps += 1

        interps_list.append({
                            "text" : interp.text,
                            "date" : interp.latte.date,
                            "likes" : likes if likes else ""
                            })

    interps_list = reversed(sorted(interps_list, key=lambda d: int(d['likes']) if d['likes'] != "" else 0))

    ## WIP calculate rank
    # interps = Interpretation.objects.order_by('latte').values_list('latte', flat=True).distinct()

    # for interp in interps:
    #     print(interp)
    rank = 1

    context = {
        't_likes' : t_likes,
        't_interps' : t_interps,
        'liked_interps' : len(Like.objects.all().filter(user=request.user)),
        'rank' : rank,
        'username' : request.user.username,
        'interpretations': interps_list
    }
    template = loader.get_template('history.html')
    return HttpResponse(template.render(context, request))

@csrf_exempt
def add_latte(request):
    """Add new latte object to database"""
    return render(request, 'addlatte.html')

@csrf_exempt
def topinterpretations(request):
    current_date = datetime.now().date()
    latte = Latte.objects.last()
    date_str = request.GET.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else current_date

    interpretations = Interpretation.objects.filter(latte=latte, created_at__date=date)

    yesterday_date = date - timedelta(days=1)  

    current_date_str = date.strftime('%Y-%m-%d')
    yesterday_date_str = yesterday_date.strftime('%Y-%m-%d')

    interps_list = []
    for interp in interpretations:
        likes = len(Like.objects.all().filter(interpretation=interp))

        is_liked_by_user = False 
        if request.user.is_authenticated:
            is_liked_by_user = bool(len(Like.objects.all().filter(interpretation=interp, user=request.user)))

        interps_list.append({
                            "text" : interp.text,
                            "user" : interp.user,
                            "likes" : likes if likes else "",
                            "inid" : interp.id,
                            "liked" : "liked" if is_liked_by_user else ""
                            })

    interps_list = reversed(sorted(interps_list, key=lambda d: int(d['likes']) if d['likes'] != "" else 0))

    context = {
        'latte': latte,
        'interpretations': interps_list,
        'date': date.strftime('%Y-%m-%d'), 
        'current_date': current_date_str,  
        'yesterday_date': yesterday_date_str,  
    }

    if request.method == 'POST':
        interp = Interpretation.objects.get(id=request.POST.get('inid'))

        if len(Like.objects.all().filter(interpretation=interp, user=request.user)) > 0:
            Like.objects.get(interpretation=interp, user=request.user).delete()
        else:
            Like.objects.create(interpretation=interp, user=request.user).save()

    template = loader.get_template('topInterpretations.html')
    return HttpResponse(template.render(context, request))

@csrf_exempt
def menu(request):
    """View function for home page of site."""
    if not request.user.is_authenticated:
        username = 'Guest'
    else:
        username = request.user.username

    if request.method == 'POST':
        logout(request)
        return redirect('/login') 
    context = {
        'quote': get_quote() if request.user.is_authenticated else "You would see some of my miraculous wisdom if you were logged in...",
        'username' : username
    }
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))

@csrf_exempt
@login_required
def accountsettings(request):
    if not request.user.is_authenticated:
        username = 'Guest'
    else:
        username = request.user.username

    if request.method == 'POST':
        return redirect('/menu') 
    template = loader.get_template('accountsettings.html')
    context = {'username' : username}
    return HttpResponse(template.render(context, request))

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