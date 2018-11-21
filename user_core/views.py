from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.db.models import Q
# Create your views here.
from authentication.views import check_user_token_validation,get_user,check_user_token_validation
from authentication.models import UserModel,DoctorModel
from doctor_core.models import Consultation


def signed_in(request):
    logged_in = check_user_token_validation(request)
    if logged_in:
        try:
            user = get_user(request)
        except:
            return logged_in
    return render(request, "patientDashboard.html")


def search_doctor(request):
    active_consultations_allowed = 1
    #doctor_specialization = request.GET.get('req_specialization_by_user')
    query = request.GET.get("query")
    doctors = None
    if query:
        doctors = DoctorModel.objects.filter(
            Q(name__icontains=query) |
        Q(specialization__icontains=query)
        ).distinct()
    else:
        doctors = DoctorModel.objects.all()
    final_list = []
    print(doctors)
    if doctors:
        for doctor in doctors:
            consultations = Consultation.objects.filter(doctor_id=doctor.id)
            #print(doctor.name)
            if consultations:
                if len([consultation for consultation in consultations if consultation.ongoing]) < active_consultations_allowed:
                    final_list.append(doctor)
            else:
                final_list.append(doctor)
    return render(request, "bookAppointment.html", {'doctors':final_list})


def go_to_chat(request):
    print(request.GET.get("doctor_id"))
    doctor_id = request.GET.get("doctor_id")
    doctor = DoctorModel.objects.filter(id=doctor_id).first()
    print(doctor)
    logged_in = check_user_token_validation(request)
    user = None
    if logged_in:
        try:
            user = get_user(request)
        except:
            return logged_in
    new_consultation = Consultation(doctor = doctor,user = user,no_days = 1)
    new_consultation.save()
    return HttpResponseRedirect("consultations/" + doctor.email_address + "/")
