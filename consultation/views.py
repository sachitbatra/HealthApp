from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.contrib import messages

from django.views.generic import DetailView, ListView

from authentication.models import UserSessionToken, DoctorSessionToken
from authentication.views import check_session_cookie, check_token_ttl, get_abstract_user

from .forms import ComposeForm
from .models import Thread, ChatMessage

from authentication.models import *
from consultation.models import *

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
