from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import User

# Create your views here.
def index(request):
    if request.method == "POST":
        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        if email == "" or password == "":
            return render(
                request,
                "assignment/login.html",
                {"message": "Please fill all the fields!"},
            )

        user = authenticate(request=request, email=email, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return render(request, "assignment/details.html")
        else:
            print(4)
            return render(
                request,
                "assignment/login.html",
                {"message": "Invalid email and/or password."},
            )
    else:
        return render(request, "assignment/login.html")


def signUp(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        pwd_confirmation = request.POST["pwd_confirmation"]
        address = request.POST["address"]

        # Ensure that all the fields are not empty
        if (
            username == ""
            or email == ""
            or pwd_confirmation == ""
            or password == ""
            or address == ""
        ):
            return render(
                request,
                "assignment/signUp.html",
                {"message": "Please fill all the fields!"},
            )

        # Ensure that password and confirmation match
        if password != pwd_confirmation:
            return render(
                request,
                "assignment/signUp.html",
                {"message": "Your passwords didn't matched!"},
            )

        # Attempt to create new user and its corresponding profile
        try:
            user = User.objects.create_user(
                name=username, email=email, password=password, address=address
            )
            user.save()

        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return redirect('login')
    else:
        return render(request, "assignment/signUp.html")


@login_required
@csrf_exempt
def edit_details(request):
    # checking that the request is sent via post
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    # getting the data that needs to be updated
    data = json.loads(request.body)

    # getting the post that needs to be updated
    updated_post = User.objects.filter(email=data.get("prev_email")).update(
        email=data.get("email"), name=data.get("username"), address=data.get("address")
    )

    # post is updated, just confirming
    return JsonResponse({"Message": "Details Updated!"}, status=201)


def logout_view(request):
    """Loging out of the website"""
    if request.method == "POST":
        logout(request)
        return redirect("login")


def delete_details(request):
    if request.method == "POST":
        email = request.POST["user_mail"]

        User.objects.filter(email=email).delete()

        return redirect('login')
