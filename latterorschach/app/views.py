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

stored_date = datetime.now().date()

@csrf_exempt
@login_required
def today(request):
    global stored_date
    dailylatte = datetime.now().date()
    try:
        latte = Latte.objects.get(date=dailylatte)
    except:
        stored_date = datetime.now().date()
        latte = None
    
    posted_already = False

    if Interpretation.objects.filter(latte=latte, user=request.user).exists():
        posted_already = True

    if request.method == 'POST' and latte:
        response = request.POST.get('response', '')
        if response:  # Only proceed if the response is not empty
            logger.info(f"{request.user.username} said \"{response}\" about latte {latte.date}")

            interpretation = Interpretation.objects.create(
                user=request.user,
                text=response,
                latte=latte
            )
            interpretation.save()  # Save the new interpretation
            return redirect('topinterpretations')  # Redirect to top interpretations after POST

    # Render the daily review template
    return render(request, 'dailyReview.html', {'latte': latte, 'posted' : posted_already})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if username and password and not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username)  # Create new user
            user.set_password(password)  # Set user password
            user.save()  # Save the new user
            return redirect('login')  # Redirect to login page after registration
        else:
            return render(request, 'errorpage.html', context = {'error_text': "Username Already Exists"})
    # Render the registration page
    return render(request, 'register.html')


@csrf_exempt
def user_login(request):
    global stored_date
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)  # Authenticate user
        if user is not None:
            login(request, user)  # Log in the user
            logger.info(f"{user.username} logged in")
            stored_date = datetime.now().date()
            return redirect('/')  # Redirect to home page
        else:
            # Return an 'invalid login' error message.
            return render(request, 'errorpage.html', context = {'error_text': "Invalid Username or Password"})
    
    # Render the login page
    return render(request, 'login.html')

@login_required  # Ensure that the user is logged in
def account(request):
    """Render the account page."""
    context = {
        'username': request.user.username,  # Pass the username to the template
    }
    return render(request, 'account.html', context)

@csrf_exempt
@login_required
def history(request):
    interpretations = Interpretation.objects.filter(user=request.user)  # Get user-specific interpretations

    t_likes = 0  # Initialize total likes
    t_interps = len(interpretations)  # Total interpretations

    interps_list = []
    for interp in interpretations:
        likes = Like.objects.filter(interpretation=interp).count()  # Get like count

        t_likes += likes  # Increment total likes
        interps_list.append({
            "text": interp.text,
            "date": interp.latte.date,
            "likes": likes if likes > 0 else "",  # Display empty if no likes
        })

    # Reverse and sort by likes, considering empty as zero
    interps_list = reversed(sorted(interps_list, key=lambda d: int(d['likes']) if d['likes'] != "" else 0))

    rank = 1  # Rank placeholder, consider further logic for ranking if required

    context = {
        't_likes': t_likes,
        't_interps': t_interps,
        'liked_interps': Like.objects.filter(user=request.user).count(),
        'rank': rank,
        'username': request.user.username,
        'interpretations': interps_list,
    }

    # Render the history page with context
    return render(request, 'history.html', context)

@csrf_exempt
def add_latte(request):
    """Add new latte object to database"""

    current_date = datetime.now().date()
    current_date_str = current_date.strftime('%Y-%m-%d')

    if request.method == 'POST':
        image_url = request.POST.get('imageurl', '')
        image_date = request.POST.get('date', '')

        logger.info(f"url: {image_url}")
        logger.info(f"date: {image_date}")

        # store to check if image is already stored for date

        if image_date:
            date = Latte.objects.filter(date=image_date)

        # error check for valid date, image exists, and if date is not already used

        if not image_date:
            return render(request, 'errorpage.html', context = {'error_text': "Invalid date entered"})
        
        if not image_url:
            return render(request, 'errorpage.html', context = {'error_text': "Invalid image URL entered"})
        
        if date:
            return render(request, 'errorpage.html', context = {'error_text': "Image already exists for entered date"})
        
        latte = Latte.objects.create(
            # use default for id
            date = image_date,
            img_url = image_url,
            user = request.user
        )
        latte.save()
        return redirect('/menu')
        
    # pass in current date to display on date picker

    context = {
        'date': current_date_str,
    }

    return render(request, 'addLatte.html', context)

@csrf_exempt
def topinterpretations(request):
    global stored_date
    date_str = request.GET.get('date', '')  # Get optional date parameter
    if not date_str:
        currentdate = stored_date
    else:
        currentdate = datetime.strptime(date_str, '%Y-%m-%d').date()
        stored_date = currentdate
    isfuture = False
    
    if currentdate > datetime.now().date():
        isfuture = True
    else:
        isfuture = False
    
    if (not isfuture) or (request.user.is_superuser or request.user.is_staff):
        try:
            latte = Latte.objects.get(date=currentdate)
        except:
            latte = None
    else:
        latte = None

    interpretations = Interpretation.objects.filter(latte=latte)  # Filter by date

    yesterday_date = currentdate - timedelta(days=1)  # Get yesterday's date
    current_date_str = currentdate.strftime('%Y-%m-%d')
    yesterday_date_str = yesterday_date.strftime('%Y-%m-%d')

    interps_list = []
    for interp in interpretations:
        likes = Like.objects.filter(interpretation=interp).count()  # Like count

        is_liked_by_user = request.user.is_authenticated and Like.objects.filter(
            interpretation=interp, user=request.user).exists()  # Check if liked by current user

        interps_list.append({
            "text": interp.text,
            "user": interp.user,
            "likes": likes if likes > 0 else "",
            "inid": interp.id,
            "liked": "liked" if is_liked_by_user else "",
        })

    # Sort and reverse by likes
    interps_list = reversed(sorted(interps_list, key=lambda d: int(d['likes']) if d['likes'] != "" else 0))

    context = {
        'latte': latte,
        'interpretations': interps_list,
        'date': current_date_str,  # Pass formatted dates
        'yesterday_date': yesterday_date_str,
        'isfuture': isfuture,
    }

    if request.method == 'POST':  # Handle like/unlike logic
        inid = request.POST.get('inid', '')  # Get interpretation ID
        if inid:  # Ensure valid ID
            interp = Interpretation.objects.get(id=inid)  # Get the interpretation
            user_like = Like.objects.filter(interpretation=interp, user=request.user)  # Check for existing like

            if user_like.exists():  # If liked, remove like
                user_like.delete()
            else:  # If not liked, add like
                Like.objects.create(interpretation=interp, user=request.user).save()
            return redirect('topinterpretations')

    # Render the top interpretations page
    return render(request, 'topInterpretations.html', context)


@csrf_exempt
def menu(request):
    """View function for home page of site."""

    if request.method == 'POST':  # Handle logout request
        global stored_date
        stored_date = datetime.now().date()
        logout(request)  # Log out the current user
        return redirect('/login')  # Redirect to login
    
    context = {
        'quote': get_quote() if request.user.is_authenticated else "You would see some of my miraculous wisdom if you were logged in...",
        'username': request.user.username if request.user.is_authenticated else 'Guest',
    }

    # Render the home page with context variables
    return render(request, 'home.html', context)


@csrf_exempt
@login_required
def accountsettings(request):
    if request.method == 'POST':  # Handle POST request
        return redirect('/menu')  # Redirect to menu page

    # Pass the current username to the template
    context = {'username': request.user.username}
    
    # Render the account settings page
    return render(request, 'accountsettings.html', context)


@csrf_exempt
@login_required
def changeusername(request):
    if request.method == 'POST':  # Handle POST request to change username
        current_user = request.user
        original_username = request.POST.get('original_username', '')
        original_password = request.POST.get('original_password', '')
        new_username = request.POST.get('new_username', '')

        user = authenticate(username=original_username, password=original_password)  # Authenticate to ensure validity
        
        if user is None or user != current_user:  # Check if valid user
            return render(request, 'errorpage.html', context = {'error_text': "Invalid username or password for the current user."})
        
        user.username = new_username  # Update the username

        try:
            user.save()  # Save the updated username
        except Exception as exception:
            return render(request, 'errorpage.html', context = {'error_text': str(exception)})
        
        return redirect('/accountsettings')  # Redirect to account settings
    
    # Render the change username page
    return render(request, 'changeusername.html')


@csrf_exempt
@login_required
def changepassword(request):
    if request.method == 'POST':  # Handle POST request for changing password
        current_user = request.user
        original_username = request.POST.get('original_username', '')
        original_password = request.POST.get('original_password', '')
        new_password = request.POST.get('new_password', '')

        user = authenticate(username=original_username, password=original_password)  # Authenticate user
        
        if user is None or user != current_user:  # Validate current user
            return render(request, 'errorpage.html', context = {'error_text': "Invalid username or password for the current user."})
        
        if not new_password:  # Check for empty new password
            return render(request, 'errorpage.html', context = {'error_text': "New password cannot be empty."})
        
        if new_password == original_password:  # Ensure passwords are different
            return render(request, 'errorpage.html', context = {'error_text': "New password shouldn't equal old password."})
        
        user.set_password(new_password)  # Set the new password
        
        try:
            user.save()  # Save the updated password
            login(request, user)  # Log the user back in after password change
        except Exception as exception:
            return render(request, 'errorpage.html', context = {'error_text': str(exception)})
        
        return redirect('/accountsettings')  # Redirect to account settings
    
    # Render the change password page
    return render(request, 'changepassword.html')

@csrf_exempt
def errorpage(request):
    """Renders error page"""
    return render(request, 'errorpage.html')