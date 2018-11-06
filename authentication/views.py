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


def user_signup_view(request):
    if request.method == "GET":
        if check_user_session_cookie(request):
            session = UserSessionToken.objects.filter(session_token=request.COOKIES.get('user_session_token')).first()
            if check_token_ttl(session):
                response = redirect('success.html')
                response['Location'] += "?msg='Your\'re already signed in!'"
                return response

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

            response = redirect('/login')
            response['Location'] += "?msg=0"
            return response

        else:
            return redirect('/error', message="Invalid Data Submitted")  # TODO: Create Error HTML File
        # TODO: Create Error View


def user_login_view(request):
    if request.method == "GET":
        if check_user_session_cookie(request):
            if check_token_ttl(request):
                response = redirect('success.html')
                response['Location'] += "?msg='Your\'re already signed in!'"
                return response

        login_form = LogInForm()

        if request.GET.get("msg") != None:
            from .message_codes import login_msg
            message_code = request.GET.get("msg")

            return render(request, 'UserLogin.html', {'form': login_form, 'message': login_msg[message_code]})
        else:
            return render(request, 'UserLogin.html', {'form': login_form})

    elif request.method == "POST":
        login_form = LogInForm(request.POST)
        response = redirect('/login')  # To be appended and returned in case of error conditions

        if login_form.is_valid():
            email = login_form.cleaned_data["email_address"]
            password = login_form.cleaned_data["password"]

            user_fromDB = UserModel.objects.filter(email_address=email).first()

            if user_fromDB:  # Not Equal to None
                if check_password(password, user_fromDB.password):
                    session_token = UserSessionToken(user=user_fromDB)
                    session_token.create_token()
                    session_token.save()

                    response = redirect('success.html')  # TODO: DashBoard
                    response.set_cookie(key="user_session_token", value=session_token.session_token)

                    return response  # TODO: Redirect to User Dashboard
                else:
                    response['Location'] += "?msg=1"
                    return response
            else:
                response['Location'] += "?msg=2"
                return response
        else:
            response['Location'] += "?msg=3"
            return response


def doc_signup_view(request):
    if request.method == "GET":
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

            img_path = os.path.join(BASE_DIR, new_doc.auth_document.url)
            img_client = ImgurClient(imgur_client_id, imgur_client_secret)
            new_doc.auth_document_url = img_client.upload_from_path(img_path, anon=True)['link']
            new_doc.save()

            send_verification_mail(name, new_doc.id, new_doc.auth_document_url)

            response = redirect('/doc/login')
            response['Location'] += "?msg=0"
            return response

        else:
            return redirect('/error', message="Invalid Data Submitted")  # TODO: Create Error HTML File
        # TODO: Create Error View


def send_verification_mail(docName, docID, imageLink):
    successLink = "http://127.0.0.1:8000/verification?id=%s&valid=y" %(docID)
    failLink = "http://127.0.0.1:8000/verification?id=%s&valid=n" %(docID)
    mail_content = "Greetings,\nValidate a new Doctor Registration to enable a better Healthcare!\nVerification Document: %s.\n To verify, please follow this link: %s.\nTo delete Doctor from System, please click here: %s." %(imageLink, successLink, failLink)

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("admin@healthapp.com")
    to_email = Email("sachitbatra97@gmail.com")
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
                messages.info(request, 'Invalid Validation URL, Please check again')
                return HttpResponseRedirect('/error')
        else:
            messages.info(request, 'Invalid Validation URL, Please check again')
            return HttpResponseRedirect('/error')


def doc_login_view(request):
    if request.method == "GET":
        login_form = LogInForm()

        if request.GET.get("msg") != None:
            from .message_codes import login_msg
            message_code = request.GET.get("msg")

            return render(request, 'DocLogin.html', {'form': login_form, 'message': login_msg[message_code]})
        else:
            return render(request, 'DocLogin.html', {'form': login_form})

    elif request.method == "POST":
        login_form = LogInForm(request.POST)
        response = redirect('/doc/login')  # To be appended and returned in case of error conditions

        if login_form.is_valid():
            email = login_form.cleaned_data["email_address"]
            password = login_form.cleaned_data["password"]

            doc_fromDB = DoctorModel.objects.filter(email_address=email).first()

            if doc_fromDB:  # Not Equal to None
                if check_password(password, doc_fromDB.password):
                    session_token = DoctorSessionToken(doctor=doc_fromDB)
                    session_token.create_token()
                    session_token.save()

                    response = redirect('success.html')  # TODO: DashBoard
                    response.set_cookie(key="doctor_session_token", value=session_token.session_token)

                    return response  # TODO: Redirect to User Dashboard
                else:
                    response['Location'] += "?msg=1"
                    return response
            else:
                response['Location'] += "?msg=2"
                return response
        else:
            response['Location'] += "?msg=3"
            return response


def check_user_token_validation(request):
    if check_user_session_cookie(request):
        session = UserSessionToken.objects.filter(session_token=request.COOKIES.get('user_session_token')).first()

        if check_token_ttl(session):
            return True
        else:
            response = redirect('/login')
            response['Location'] += "?msg=4"
            return response
    else:
        response = redirect('/login')
        response['Location'] += "?msg=5"
        return response


def check_doc_token_validation(request):
    if check_doc_session_cookie(request):
        session = DoctorSessionToken.objects.filter(session_token=request.COOKIES.get('user_session_token')).first()

        if check_token_ttl(session):
            return True
        else:
            response = redirect('/doc/login')
            response['Location'] += "?msg=4"
            return response
    else:
        response = redirect('/doc/login')
        response['Location'] += "?msg=5"
        return response


def check_user_session_cookie(request):
    if request.COOKIES.get('user_session_token') is not None:
        return True
    else:
        return False


def check_doc_session_cookie(request):
    if request.COOKIES.get('doctor_session_token') is not None:
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
    return UserSessionToken.objects.filter(session_token=request.COOKIES.get('user_session_token')).first().user


def get_doctor(request):
    return DoctorSessionToken.objects.filter(session_token=request.COOKIES.get('user_session_token')).first().doctor