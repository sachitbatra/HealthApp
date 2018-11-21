from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.contrib import messages

from django.views.generic import DetailView, ListView

import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from authentication.models import UserSessionToken, DoctorSessionToken
from authentication.views import check_session_cookie, check_token_ttl, get_abstract_user

from .forms import ComposeForm,GoogleFitDataForm
from .models import Thread, ChatMessage

from imgurpython import ImgurClient
from authentication.api_keys import imgur_client_id, imgur_client_secret

from authentication.models import *
from consultation.models import *

from random import randint

import os

class InboxView(ListView):
    template_name = 'inbox.html'
    def get_queryset(self):
        if get_abstract_user(self.request) is not None:
            user = get_abstract_user(self.request)
        else:
            messages.info(self.request, 'Please Log in first to access the page')
            return HttpResponseRedirect('/login')
        return Thread.objects.by_user(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if get_abstract_user(self.request) is not None:
            curUser = get_abstract_user(self.request)
            context['curUser'] = curUser.email_address
        return context

    def dispatch(self, request, *args, **kwargs):
        if get_abstract_user(request) is None:
            messages.error(request, 'Please log in first to access Inbox.')
            return HttpResponseRedirect('/login')
        else:
            return super(InboxView, self).dispatch(request, *args, **kwargs)

class ThreadView(FormMixin, DetailView):
    template_name = 'thread.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        user = None
        if get_abstract_user(self.request) is not None:
            user = get_abstract_user(self.request)
        return Thread.objects.by_user(user)

    def get_object(self):
        other_username = self.kwargs.get("username")

        user = None
        if get_abstract_user(self.request) is not None:
            user = get_abstract_user(self.request)

        obj, created = Thread.objects.get_or_new(user, other_username)
        if obj is None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()

        if get_abstract_user(self.request) is not None:
            curUser = get_abstract_user(self.request)
            context['curUser'] = curUser.email_address
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = None

        if get_abstract_user(self.request) is not None:
            user = get_abstract_user(self.request)

        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if get_abstract_user(request) is None:
            messages.error(request, 'Please log in first to access Inbox.')
            return HttpResponseRedirect('/login')
        else:
            return super(ThreadView, self).dispatch(request, *args, **kwargs)



def select_doctor(request):
    active_consultations_allowed = 1
    doctor_specialization = request.GET.get('req_specialization_by_user')
    query = DoctorModel.objects.all()
    print(query)
    doctor_info = []
    for doctor in query:
        doctor_info += [(doctor.name,doctor.specialization)]
    doctors_with_specialization = DoctorModel.valid_doctors_objects.valid_doctors(doctor_specialization)
    valid_doctor_emails = []
    for doctor in doctors_with_specialization:
        active_doctor_consultations = Thread.objects.num_doctor_consultations(doctor.email_address)
        if(active_doctor_consultations<= active_consultations_allowed):
            valid_doctor_emails+=[(doctor.email_address,doctor.name)]
    print("emails are:",valid_doctor_emails)
    args = {'doctors_in_db' :doctor_info, 'ids':valid_doctor_emails}
    return render(request, 'select_doctor.html' ,args)

'''
def upload_google_fit_data(request):
    fit_data_upload_form = GoogleFitDataForm(request.POST,request.FILES)
    email_address = fit_data_upload_form["email_address"]
    google_fit_data = fit_data_upload_form["google_fit_data"]
    new_data = GoogleFitVisualisation(email_id = email_address, health_data_file = google_fit_data)
    new_data.save()
    img_path = new_data.auth_document.path
    img_client = ImgurClient(imgur_client_id, imgur_client_secret)
    new_data.auth_document_url = img_client.upload_from_path(img_path, anon=True)['link']
    new_data.save()
    return render('consultation/upload_google_fit_data.html')'''


def google_fit(request):
    if(request.method == "GET"):
        print("---------I AM IN GET------------")
        upload_form = GoogleFitDataForm()
        return render(request,'upload_google_fit_data.html',{'form':upload_form})

    elif(request.method== "POST"):
        upload_form = GoogleFitDataForm(request.POST, request.FILES)
        print("---------I AM IN POST ------------")
        upload_form.is_valid()
        user_id = get_abstract_user(request)
        print(user_id)
        data = upload_form.cleaned_data["health_data_file"]
        print(data)
        new_data = GoogleFitVisualisation(user = user_id,email_id = user_id.email_address , health_data_file = data)
        new_data.save()
        img_path = new_data.health_data_file.path
        new_data.health_data_url = img_path
        new_data.save()
        return HttpResponseRedirect('/consultation/google_fit_data_visualisation')

def bar_plot_with_feature(path, random_number, filename,feature_name,interval):
    data = pd.read_csv(filename, usecols=['Date',feature_name], parse_dates=['Date'])
    data.set_index('Date',inplace=True)
    fig, ax = plt.subplots(figsize=(15,7))
    if(interval=='full_history'):
        ax.bar(data.index, data[feature_name])
        ax.xaxis.set_major_locator(mdates.WeekdayLocator())
    else:
        ax.bar(data.index[-(interval):], data[feature_name][-(interval):])
        ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.ylabel("{}".format(feature_name))
    plt.xticks(rotation=90)
    full_path = path + '/' + str(random_number) + '_' + feature_name.split()[0] + '.png'
    plt.savefig(full_path)
    plt.close()
    temp_path = "/media/GoogleFitData/"
    path_to_return = temp_path + str(random_number) + '_' + feature_name.split()[0] + '.png'
    return(path_to_return)



def google_fit_data_visualisation(request):
    user = get_abstract_user(request)
    filename = GoogleFitVisualisation.objects.all().filter(email_id = user.email_address).values_list('health_data_url', flat=True)
    number = len(filename[0].split('/'))
    path = '/'.join(filename[0].split('/')[:(number-1)])
    print(path)
    random_number = randint(1,100000)
    important_features = ['Calories (kcal)', 'Distance (m)',
                      'Step count', 'Inactive duration (ms)',
                      'Walking duration (ms)']

    path_dict = {}

    for feature in important_features:
        img_path = bar_plot_with_feature(path, random_number, filename[0], feature, 10)
        temp = {feature:img_path}
        path_dict.update(temp)
    args = {'img_path':path_dict}
    return render(request, 'google_fit_data_visualisation.html', args )
