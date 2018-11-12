from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.utils import timezone
from datetime import timedelta
from django.http import Http404
import json
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserModelSerializer

from HealthApp.settings import BASE_DIR
from imgurpython import ImgurClient
from .api_keys import imgur_client_id, imgur_client_secret

import sendgrid
import os
from sendgrid.helpers.mail import *


def error_view(request):
    return render(request, 'Error.html')


class UserOperations(APIView):
    def get(self, request):
        if request.GET.get("email") is not None:
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
            if input_json[curField] is None:
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


def user_signup_view(request):
    if request.method == "GET":
        if check_session_cookie(request):
            session = UserSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first()
            if check_token_ttl(session):
                messages.info(request, 'Your\'re already signed in as a User!')
                return HttpResponseRedirect('/error')  # TODO: Replace with Homepage

        signup_form = UserSignUpForm()
        return render(request, 'UserRegister.html', {'form': signup_form})

    elif request.method == "POST":
        signup_form = UserSignUpForm(request.POST)

        if signup_form.is_valid():
            name = signup_form.cleaned_data["name"]
            email_id = signup_form.cleaned_data["email_address"]
            password = signup_form.cleaned_data["password"]
            dateOfBirth = signup_form.cleaned_data["dateOfBirth"]

            new_user = UserModel(name=name, email_address=email_id, dateOfBirth=dateOfBirth, password=make_password(password))
            new_user.save()

            messages.info(request, 'Successfully Signed Up, Please enter your details again to Log in')
            return HttpResponseRedirect('/login')

        else:
            messages.error(request, 'Invalid Data Submitted')
            return HttpResponseRedirect('/error')


def user_login_view(request):
    if request.method == "GET":
        if check_session_cookie(request):
            sessionVar = UserSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first()
            userType = "User"
            if sessionVar is None:
                sessionVar = DoctorSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first()
                userType = "Doctor"
            if check_token_ttl(sessionVar):
                messages.info(request, f"You\'re already signed in as a {userType}!")
                return HttpResponseRedirect('/error')  # TODO: Replace with Homepage

        login_form = LogInForm()
        return render(request, 'UserLogin.html', {'form': login_form})

    elif request.method == "POST":
        login_form = LogInForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data["email_address"]
            password = login_form.cleaned_data["password"]

            user_fromDB = UserModel.objects.filter(email_address=email).first()

            if user_fromDB:
                if check_password(password, user_fromDB.password):
                    session_token = UserSessionToken(user=user_fromDB)
                    session_token.create_token()
                    session_token.save()

                    request.session['session_token'] = session_token.session_token  # Using Session Middleware
                    response = redirect('success.html')  # TODO: DashBoard
                    # response.set_cookie(key="session_token", value=session_token.session_token)
                    return response  # TODO: Redirect to User Dashboard
                else:
                    messages.error(request, 'Invalid Password, please try again')
                    return HttpResponseRedirect('/login')
            else:
                messages.error(request, 'No Registered User found with the given Email Address')
                return HttpResponseRedirect('/login')
        else:
            messages.error(request, 'Invalid Data Submitted in Log In Form')
            return HttpResponseRedirect('/login')


def doc_signup_view(request):
    if request.method == "GET":
        if check_session_cookie(request):
            sessionVar = UserSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first()
            userType = "User"
            if sessionVar is None:
                sessionVar = DoctorSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first()
                userType = "Doctor"
            if check_token_ttl(sessionVar):
                messages.info(request, f"You\'re already signed in as a {userType}!")
                return HttpResponseRedirect('/error')  # TODO: Replace with Homepage

        signup_form = DocSignUpForm()
        return render(request, 'DocRegister.html', {'form': signup_form})

    elif request.method == "POST":
        signup_form = DocSignUpForm(request.POST, request.FILES)

        if signup_form.is_valid():
            name = signup_form.cleaned_data["name"]
            email_id = signup_form.cleaned_data["email_address"]
            password = signup_form.cleaned_data["password"]
            dateOfBirth = signup_form.cleaned_data["dateOfBirth"]
            specialization = signup_form.cleaned_data["specialization"]
            auth_document = signup_form.cleaned_data["auth_document"]
            degree = signup_form.cleaned_data["degree"]
            experience = signup_form.cleaned_data["experience"]

            new_doc = DoctorModel(name=name, email_address=email_id, dateOfBirth=dateOfBirth, password=make_password(password), specialization=specialization, auth_document=auth_document, degree=degree, experience=experience)
            new_doc.save()

            img_path = new_doc.auth_document.path
            img_client = ImgurClient(imgur_client_id, imgur_client_secret)
            new_doc.auth_document_url = img_client.upload_from_path(img_path, anon=True)['link']
            new_doc.save()

            #send_verification_mail(name, new_doc.id, new_doc.auth_document_url)

            messages.info(request, 'Successfully Signed Up, Please enter your details again to Log in')
            return HttpResponseRedirect('/doc/login')
        else:
            messages.error(request, 'Invalid data entered')
            return HttpResponseRedirect('/error')


def send_verification_mail(docName, docID, imageLink):
    successLink = "http://127.0.0.1:8000/verification?id=%s&valid=y" %(docID)
    failLink = "http://127.0.0.1:8000/verification?id=%s&valid=n" %(docID)
    mail_content = "Greetings,\nValidate a new Doctor Registration to enable a better Healthcare!\nVerification Document: %s.\n To verify, please follow this link: %s.\nTo delete Doctor from System, please click here: %s." %(imageLink, successLink, failLink)

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("admin@healthapp.com")
    to_email = Email("sidd.suresh97@gmail.com")
    subject = "Verify New Dcotor: " + docName
    content = Content("text/plain", mail_content)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


def verify_doctor(request):
    if request.method == "GET":
        if request.GET.get("id") != None:
            curDoctor = DoctorModel.objects.get(id=request.GET.get("id"))

            if request.GET.get("valid") != None:
                if request.GET.get("valid") == "y":
                    curDoctor.verified = True
                    curDoctor.save()
                    messages.info(request, 'Validation Successful')
                else:
                    curDoctor.delete()
                    messages.info(request, 'Deletion Successful')
                return HttpResponseRedirect('/doc')  #TODO: Replace with HomePage
            else:
                messages.error(request, 'Invalid Validation URL, Please check again')
                return HttpResponseRedirect('/error')
        else:
            messages.error(request, 'Invalid Validation URL, Please check again')
            return HttpResponseRedirect('/error')


def doc_login_view(request):
    if request.method == "GET":
        if check_session_cookie(request):
            sessionVar = UserSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first()
            userType = "User"
            if sessionVar is None:
                sessionVar = DoctorSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first()
                userType = "Doctor"
            if check_token_ttl(sessionVar):
                messages.info(request, f"You\'re already signed in as a {userType}!")
                return HttpResponseRedirect('/error')  # TODO: Replace with Homepage

        login_form = LogInForm()
        return render(request, 'DocLogin.html', {'form': login_form})

    elif request.method == "POST":
        login_form = LogInForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data["email_address"]
            password = login_form.cleaned_data["password"]

            doc_fromDB = DoctorModel.objects.filter(email_address=email).first()

            if doc_fromDB:
                if check_password(password, doc_fromDB.password):
                    session_token = DoctorSessionToken(user=doc_fromDB)
                    session_token.create_token()
                    session_token.save()

                    request.session['session_token'] = session_token.session_token
                    response = redirect('/doctor/signed_in')  # TODO: DashBoard
                    # response.set_cookie(key="session_token", value=session_token.session_token)

                    return response  # TODO: Redirect to User Dashboard
                else:
                    messages.error(request, 'Invalid Password, please try again')
                    return HttpResponseRedirect('/doc/login')
            else:
                messages.error(request, 'No Registered User found with the given Email Address')
                return HttpResponseRedirect('/doc/login')
        else:
            messages.error(request, 'Invalid Data Submitted in Log In Form')
            return HttpResponseRedirect('/doc/login')


def logout_view(request):
    if request.method == "GET":
        del request.session['session_token']
        request.session.modified = True
        return HttpResponseRedirect('/login')
    else:
        raise Http404


def check_user_token_validation(request):
    if check_session_cookie(request):
        session = UserSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first()

        if check_token_ttl(session):
            return True
        else:
            messages.error(request, 'Your Session has expired, please log in again to continue')
            return HttpResponseRedirect('/login')
    else:
        messages.info(request, 'Please Log in first to access the page')
        return HttpResponseRedirect('/login')


def check_doc_token_validation(request):
    if check_doc_session_cookie(request):
        session = DoctorSessionToken.objects.filter(session_token=request.session.get('session_token')).first()

        if check_token_ttl(session):
            return True
        else:
            messages.error(request, 'Your Session has expired, please log in again to continue')
            return HttpResponseRedirect('/doc/login')
    else:
        messages.info(request, 'Please Log in first to access the page')
        return HttpResponseRedirect('/doc/login')


def check_session_cookie(request):
    if request.session.get('session_token') is not None:
        return True
    else:
        return False


# Backward compatibility: use check_session_cookie function instead
def check_user_session_cookie(request):
    if request.session.get('session_token') is not None:
        return True
    else:
        return False


# Backward compatibility: use check_session_cookie function instead
def check_doc_session_cookie(request):
    if request.session.get('session_token') is not None:
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


# Backward compatibility: use get_abstract_user function instead
def get_user(request):
    return UserSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first().user


# Backward compatibility: use get_abstract_user function instead
def get_doctor(request):
    return DoctorSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first().user


# Returns the User (Doctor or User) if logged in, None otherwise
def get_abstract_user(request):
    if check_session_cookie(request):
        sessionVar = UserSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first()
        if sessionVar is None:
            sessionVar = DoctorSessionToken.objects.filter(session_token=request.session.get('session_token', None)).first()
        if check_token_ttl(sessionVar):
            return sessionVar.user
        return None
