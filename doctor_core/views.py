from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import CreateProfile
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
# Create your views here.
from authentication.views import check_doc_token_validation,get_doctor

from authentication.models import DoctorModel
from .models import DoctorProfile,Consultation,FeedBack

def signed_in(request):
    logged_in = check_doc_token_validation(request)
    doctor = None
    if logged_in:
        try:
            doctor = get_doctor(request)
        except:
            #messages.error(request,"Something went wrong in getting the doctor data")
            return HttpResponse("Looks like something went wrong!")
        return render(request,"dashboard.html",{"doctor":doctor})
    return HttpResponse("Looks like something went wrong!")

def view_profile(request):
    logged_in = check_doc_token_validation(request)
    doctor = None
    if logged_in:
        try:
            doctor = get_doctor(request)
        except:
            return HttpResponse("Looks like something went wrong!")
    profile =   DoctorProfile.objects.filter(user_id = doctor.id).first()
    if profile:
        return render(request,"success.html",{'profile':profile})
    else:
        return redirect('/doctor/create_profile')

def create_profile(request):
    if request.method == 'GET':
        profile_form = CreateProfile()
    elif request.method == 'POST':
        profile_form = CreateProfile(request.POST,request.FILES)
        doctor = None
        if profile_form.is_valid():
            try:
                doctor = get_doctor(request)
            except:
                return HttpResponse("Looks like something went wrong in retrieving the user details from session database")
            bio = profile_form.cleaned_data["bio"]
            phone_no = profile_form.cleaned_data["phone_no"]
            image = profile_form.cleaned_data["image"]
            profile = DoctorProfile(user = doctor, bio = bio,phone_no = phone_no,image = image)
            profile.save()
            response = redirect('/doctor/view_profile')
            return response
        else:
            #return redirect('/error', message="Invalid Data Submitted")  # TODO: Create Error HTML File
            return render(request,'error.html',{'message':"Invalid Data Submitted"})
    return render(request,'profile_creation.html',{'form':profile_form})

def edit_profile(request):
    if request.method == 'GET':
        doctor = None
        try:
            doctor = get_doctor(request)
        except:
            return HttpResponse("Looks like something went wrong in retrieving the user details from session database")
        profile = DoctorProfile.objects.filter(user_id = doctor.id).first()
        profile_form = CreateProfile(request.POST or None,initial={'bio':profile.bio,'phone_no':profile.phone_no,'image':profile.image})
    elif request.method == 'POST':
        profile_form = CreateProfile(request.POST,request.FILES)
        doctor = None
        if profile_form.is_valid():
            try:
                doctor = get_doctor(request)
            except:
                return HttpResponse("Looks like something went wrong in retrieving the user details from session database")
        profile = DoctorProfile.objects.filter(user_id = doctor.id).first()
        if profile_form.cleaned_data["bio"]:
            profile.bio = profile_form.cleaned_data["bio"]
        if profile_form.cleaned_data["phone_no"]:
            profile.phone_no = profile_form.cleaned_data["phone_no"]
        if profile_form.cleaned_data["image"]:
            profile.image = profile_form.cleaned_data["image"]
        profile.save()
        response = redirect('/doctor/view_profile')
        return response
    return render(request,"profile_edit.html",{'form':profile_form})

def view_ongoing_consultations(request):
    logged_in = check_doc_token_validation(request)
    doctor = None
    if logged_in:
        try:
            doctor = get_doctor(request)
        except:
            #messages.error(request,"Something went wrong in getting the doctor data")
            return HttpResponse("Looks like something went wrong!")
        consultations = Consultation.objects.filter(doctor_id = doctor.id)
        ongoing_consultations = [consultation  for consultation in consultations if consultation.ongoing]
        return render(request,"current_consultations.html",{'consultations':ongoing_consultations})

def view_past_consultations(request):
    logged_in = check_doc_token_validation(request)
    doctor = None
    if logged_in:
        try:
            doctor = get_doctor(request)
        except:
            return HttpResponse("Looks like something went wrong!")
        consultations = Consultation.objects.filter(doctor_id = doctor.id)
        past_consultations_list = [consultation for consultation in consultations if not consultation.ongoing]
        paginator = Paginator(past_consultations_list,5)
        page = request.GET.get('page')
        past_consultations = paginator.get_page(page)
        return render(request,"past_consultations.html",{'consultations':past_consultations})

def view_feedback(request):
    logged_in = check_doc_token_validation(request)
    doctor = None
    if logged_in:
        try:
            doctor = get_doctor(request)
        except:
            return logged_in
        feedback_list = FeedBack.objects.filter(consultation__doctor_id = doctor.id)
        paginator = Paginator(feedback_list,5)
        page = request.GET.get('page')
        feedback = paginator.get_page(page)
        return render(request, "review.html",{'reviews':feedback})

def view_stats(request):
    logged_in = check_doc_token_validation(request)
    doctor = None
    if logged_in:
        try:
            doctor = get_doctor(request)
        except:
            return logged_in
        return render(request,"statistic.html")