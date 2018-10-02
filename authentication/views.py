from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import SignUpForm
from .models import *

def signup_view(request):
    if request.method == "GET":
        signup_form = SignUpForm()

    elif request.method == "POST":
        signup_form = SignUpForm(request.POST)

        if signup_form.is_valid():
            name = signup_form.cleaned_data["name"]
            email_id = signup_form.cleaned_data["email_address"]
            password = signup_form.cleaned_data["password"]
            age = signup_form.cleaned_data["age"]

            new_user = UserModel(name=name, email_address=email_id, age=age, password=make_password(password))
            new_user.save()

            return redirect('login')

        else:
            return render(request, 'error.html', {'message': "Invalid Data Submitted"})  # TODO: Create Error HTML File

    return render(request, 'register.html', {'form': signup_form})