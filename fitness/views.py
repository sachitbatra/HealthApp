from django.views.generic import ListView,UpdateView
from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect,HttpResponse
from .forms import RoutineForm,ScheduleForm
from .models import Routines,Schedule
from authentication.views import check_user_token_validation,get_user
from django.contrib import messages
# from .forms import RoutineForm


#from .forms import *
# Create your views here
def schedule_form(request):
    logged_in = check_user_token_validation(request)
    user = None
    if logged_in:
        try:
            user = get_user(request)
        except:
            #messages.error(request,"Something went wrong in getting the doctor data")
            return HttpResponse("Looks like something went wrong!")
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            time_from = form.cleaned_data["endtime"]
            time_to = form.cleaned_data["starttime"]
            new_sched = Schedule(user=user,name=name,starttime=time_from,endtime=time_to)
            new_sched.save()
            messages.info(request, 'Added new Schedule')
            return HttpResponseRedirect('/fitness/view_schd')
        else:
            messages.error(request,'Whoops there was an error in the data submitted!')
            return HttpResponseRedirect('/fitness/schedule')
    else:
        form = ScheduleForm()
    return render(request,'fitness/fitform.html',{'form':form})

def routine_form(request,schd_id):
    # model = Routines
    # fields = ['exc','sets','reps']
    # success_url = reverse_lazy('fitform')
    logged_in = check_user_token_validation(request)
    user = None
    if logged_in:
        try:
            user = get_user(request)
        except:
            #messages.error(request,"Something went wrong in getting the doctor data")
            return HttpResponse("Looks like something went wrong!")

    if request.method == 'POST':
        form = RoutineForm(request.POST)
        if form.is_valid():
            sets = form.cleaned_data["sets"]
            reps = form.cleaned_data["reps"]
            exc = form.cleaned_data["exc"]
            new_rtn = Routines(exc = exc,sets = sets, reps = reps, schd = get_object_or_404(Schedule,pk=schd_id))
            new_rtn.save()
            messages.info(request, 'Added new Routine')
            return HttpResponseRedirect('/fitness/%s/view_rtns'%schd_id)
        else:
            messages.error(request,'Whoops there was an error in the data submitted!')
            return HttpResponseRedirect('/fitness/%s/rtn'%schd_id)
    else:
        form = RoutineForm()
    return render(request,'fitness/fitform.html',{'form':form})

class display_schedules(ListView):
    model = Schedule
    context_object_name = 'scheds'

class display_routines(ListView):
    model = Routines
    context_object_name = 'rtns'
    def get_queryset(self):
        return Routines.objects.filter(schd__id=self.kwargs['schd_id'])
