import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User

def index(request):    
    if request.user.is_authenticated:    	
    	return render(request, "quiz/main.html")
    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("front"))

				#	Home Page

def front(request):
	return render(request, "quiz/home.html")


				#	Registration Process

def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        first_name = request.POST["f_name"] + " " + request.POST["l_name"]     
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "quiz/register.html", {
                "message": "Passwords must match."
            })

        # 	Attempt to create new user
        try:
            user = User.objects.create_user(
            	first_name, email, password)
            user.save()         
        except IntegrityError as e:
            #print(e)
            return render(request, "quiz/register.html", {
                "message": "User has already registered."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "quiz/register.html")      


				#	Login View

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "quiz/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "quiz/login.html")        


#	.......	Logout

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))



#  Recover

def recover(request):
    if request.method == "POST":
        email = request.POST["email"]
        new_pass = request.POST["password"]
        u = User.objects.get(email=email)
        u.set_password(new_pass)
        u.save()
        return render(request, "quiz/pass.html", {
                "message": "If You'r registerd than your password updated successfully."
            })        
    else:
        return render(request, "quiz/pass.html")        