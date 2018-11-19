from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.db.models import Q
# Create your views here.
from authentication.views import check_user_token_validation,get_user
from authentication.models import UserModel,DoctorModel
from doctor_core.models import Consultation
# Create your views here.
def signed_in(request):
    logged_in = check_user_token_validation(request)
    if logged_in:
        try:
            user = get_user(request)
        except:
            return logged_in
    return render(request,"patientDashboard.html")

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
    final_list = []
    print(doctors)
    if doctors:
        for doctor in doctors:
            consultations = Consultation.objects.filter(doctor_id = doctor.id)
            #print(doctor.name)
            if consultations:
                if not [consultation for consultation in consultations if consultation.ongoing]:
                    final_list.append(doctor)
            else:
                final_list.append(doctor)
    return render(request,"bookAppointment.html",{'doctors':final_list})

def go_to_chat(request):
    pass



    
