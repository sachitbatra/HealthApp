from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.utils import timezone
from datetime import timedelta


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

            response = redirect('/login')
            response['Location'] += "?msg=0"
            return response

        else:
            return redirect('/error', message="Invalid Data Submitted")  # TODO: Create Error HTML File
        # TODO: Create Error View

    return render(request, 'register.html', {'form': signup_form})


def login_view(request):
    if request.method == "GET":
        login_form = LogInForm()

        if request.GET.get("msg") != None:
            from .message_codes import login_msg
            message_code = request.GET.get("msg")

            return render(request, 'login.html', {'form': login_form, 'message': login_msg[message_code]})
        else:
            return render(request, 'login.html', {'form': login_form})

    elif request.method == "POST":
        login_form = LogInForm(request.POST)
        response = redirect('/login')  # To be appended and returned in case of error conditions

        if login_form.is_valid():
            email = login_form.cleaned_data["email_address"]
            password = login_form.cleaned_data["password"]

            user_fromDB = UserModel.objects.filter(email_address=email).first()

            if user_fromDB:  # Not Equal to None
                if check_password(password, user_fromDB.password):
                    session_token = SessionToken(user=user_fromDB)
                    session_token.create_token()
                    session_token.save()

                    response = redirect('success.html') #TODO: DashBoard
                    response.set_cookie(key="session_token", value=session_token.session_token)

                    return response
                else:
                    response['Location'] += "?msg=1"
                    return response
            else:
                response['Location'] += "?msg=2"
                return response
        else:
            import pdb
            pdb.set_trace()
            response['Location'] += "?msg=3"
            return response


def check_token_validation(request):
    if check_session_cookie(request):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()

        if check_token_ttl(session):
            return True
        else:
            redirect('/login', message="Your Session has expired, please log in again to continue:")
    else:
        redirect('/login', message="Please Log in first to access that page:")


def check_session_cookie(request):
    if request.COOKIES.get('session_token'):
        return True
    else:
        return False


def check_token_ttl(token):
    time_to_live = token.created_on + timedelta(days=1)

    if time_to_live > timezone.now():
        return True
    else:
        token.delete()
        return False


def get_user(request):
    return SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first().user
