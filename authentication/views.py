from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.utils import timezone
from datetime import timedelta
from django.http import Http404
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserModelSerializer

class UserOperations(APIView):
    def get(self, request):
        if request.GET.get("email") != None:
            email = request.GET.get("email")
            curUser = UserModel.objects.filter(email_address=email).first()

            if curUser != None:
                serializer = UserModelSerializer(curUser)
                return Response(serializer.data)
            else:
                raise Http404
        else:
            raise Http404

    def post(self, request):
        fields = ['name', 'email_address', 'password', 'age', 'created_on']

        input_json = json.loads(request.body)

        for curField in fields:
            if input_json[curField] == None:
                raise Http404

        user_name = input_json['name']
        user_email = input_json['email']
        user_password = input_json['password']
        user_age = input_json['age']

        existing_user = UserModel.objects.filter(email_address=user_email).first()

        if existing_user:
            raise Http404

        else:
            new_user = UserModel(name=user_name, email_address=user_email, age=user_age, password=user_password)
            new_user.save()


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
