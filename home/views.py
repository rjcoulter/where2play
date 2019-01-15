from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.middleware.csrf import get_token
from django.db.models import F
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

import json
import datetime
import pytz
from django.utils import timezone
import re

from .models import Facility, Court, Reserved_Time_Slot, Time_Slot
from .forms import SignUpForm


def HomePageView(request):
    facilities = Facility.objects.all()
    gym = Facility.objects.all().filter(F_Type='Gym')
    outdoors = Facility.objects.all().filter(F_Type='Field')
    other = Facility.objects.all().filter(F_Type='Other Facility')
    gym, outdoors, other = add_unique_ids_field(gym, outdoors, other)
    return render(request, 'index.html', {'facilities': facilities, 'Gym': gym, 'Outdoors': outdoors, 'Others': other, })

def add_unique_ids_field(gym, outdoors, other):
    for i in gym:
        final_name = ""
        name = i.F_Name.split()
        for j in name:
            if j != "&" and j.find("'") == -1:
                final_name += j
        i.name_no_space = final_name
    for i in outdoors:
        final_name = ""
        name = i.F_Name.split()
        for j in name:
            if j != "&" and j.find("'") == -1:
                final_name += j
        i.name_no_space = final_name
    for i in other:
        final_name = ""
        name = i.F_Name.split()
        for j in name:
            if j != "&" and j.find("'") == -1:
                final_name += j
        i.name_no_space = final_name
    return gym, outdoors, other


class AboutPageView(TemplateView):
    template_name = "about.html"


class ContactPageView(TemplateView):
    template_name = "contact.html"

    def post(self, request, *args, **kwargs):
        context = request.POST
        print(context)
        send_mail(
            'Customer Contact from ' + context['firstname'], # subject
            'Customer First Name: ' + context['firstname'] + '\n' +
            'Customer E-Mail: ' + context['form[email]'] + '\n' +
            'Customer Feedback: ' + context['form[comments]'],
            settings.EMAIL_HOST_USER, # email to send from
            [settings.EMAIL_HOST_USER] # recipient
        )
        
        return redirect('/')


class LoginPageView(TemplateView):
    template_name = "login.html"


class SignupPageView(TemplateView):
    template_name = "signup.html"


class SchedulerPageView(TemplateView):
    template_name = "scheduler.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'test': 'test'})

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            days = request.POST.get('days')
            date = request.POST.get('date')
            court = request.POST.get('court')
            facility = request.POST.get('facility')
            times = {}
            availabilityTimes = {}
            courtAvailability = {}

            aTimes = Time_Slot.objects.filter(court_id=court)

            for aS in aTimes:
                time = aS.time
                aSdate = aS.date

                timeStr = time.strftime('%H%M')
                dateStr = aSdate.strftime('%Y-%m-%d')

                if not dateStr in availabilityTimes:
                    availabilityTimes[dateStr] = {timeStr: aS.signup_count}
                else:
                    availabilityTimes[dateStr][timeStr] = aS.signup_count

                if not dateStr in courtAvailability:
                    courtAvailability[dateStr] = {timeStr: aS.available}
                else:
                    courtAvailability[dateStr][timeStr] = aS.available

            json_aList = json.dumps(availabilityTimes)
            json_court_availability = json.dumps(courtAvailability)

            courtObject = Court.objects.filter(id=court)
            
            return render(request, 'availabilitySchedule.html', {'date': date, 'days': days, 'facility': facility, 'court': court, 'aJson_list': json_aList, 'courtObject': courtObject, 'json_court_availability': courtAvailability})

        days = request.POST.get('days')
        date = request.POST.get('date')
        court = request.POST.get('court')
        facility = request.POST.get('facility')
        times = {}
        availabilityTimes = {}
        courtAvailability = {}

        user_id = request.user.id
        user = User.objects.get(pk=user_id)

        t = Reserved_Time_Slot.objects.filter(
            person_id=user.our_user.id, court_id=court, facility_id=facility)
        aTimes = Time_Slot.objects.filter(court_id=court)

        for s in t:
            time = s.time
            sDate = s.date

            timeStr = time.strftime('%H%M')
            dateStr = sDate.strftime('%Y-%m-%d')

            if not dateStr in times:
                times[dateStr] = [timeStr]
            else:
                times[dateStr].append(timeStr)

        for aS in aTimes:
            time = aS.time
            aSdate = aS.date

            timeStr = time.strftime('%H%M')
            dateStr = aSdate.strftime('%Y-%m-%d')

            if not dateStr in availabilityTimes:
                availabilityTimes[dateStr] = {timeStr: aS.signup_count}
            else:
                availabilityTimes[dateStr][timeStr] = aS.signup_count

            if not dateStr in courtAvailability:
                courtAvailability[dateStr] = {timeStr: aS.available}
            else:
                courtAvailability[dateStr][timeStr] = aS.available

        json_aList = json.dumps(availabilityTimes)
        json_court_availability = json.dumps(courtAvailability)

        print(courtAvailability)

        json_list = json.dumps(times)
        json_aList = json.dumps(availabilityTimes)
        
        courtObject = Court.objects.filter(id=court)
        
        return render(request, self.template_name, {'date': date, 'days': days, 'facility': facility, 'court': court, 'json_list': json_list, 'aJson_list': json_aList, 'courtObject': courtObject, 'json_court_availability': courtAvailability})


def load_court_types(request):
    facility = request.GET.get('facility')
    courts = Court.objects.filter(facility__F_Name=facility)
    return render(request, 'court_type_options.html', {'courts': courts})


def convertTime(time):
    if len(time) == 3:
        time = '0' + time

    hour = int(time[0:2])
    minutes = int(time[2:])

    return (hour, minutes)


def signUpForTimes(request):
    data = json.loads(request.body)
    user_id = request.user.id
    user = User.objects.get(pk=user_id)

    userTimeSlots = Reserved_Time_Slot.objects.filter(
        person_id=user.our_user.id, court_id=data['court'])
    for timeSlot in userTimeSlots:
        Time_Slot.objects.filter(date=timeSlot.date, time=timeSlot.time, court_id=data['court']).update(
            signup_count=F('signup_count') - 1)

    userTimeSlots.delete()

    for d in data['times']:
        dateString = d.split('-')
        date = datetime.datetime(int(dateString[0]), int(
            dateString[1]) + 1, int(dateString[2]))
        for signUpTime in data['times'][d]:
            h, m = convertTime(signUpTime)
            time = datetime.time(h, m)
            Time_Slot.objects.filter(date=date, time=time, court_id=data['court']).update(
                signup_count=F('signup_count') + 1)
            r = user.our_user.reserved_time_slot_set.create(
                court_id=data['court'],
                facility_id=data['facility'],
                date=date,
                time=time,
            )

    json_list = json.dumps(data['json_list'])
    json_aList = json.dumps(data['aJson_list'])
    return render(request, "scheduler.html", {'date': data['date'], 'days': data['days'], 'facility': data['facility'], 'court': data['court'], 'json_list': json_list, 'aJson_list': json_aList})


def logout_user(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print('okay')
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            rawPassword = form.cleaned_data.get('password')
            user = authenticate(request, username=username,
                                password=rawPassword)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})
