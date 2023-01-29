from django.shortcuts import render,redirect,get_object_or_404
from calendar_app.models import Event, EventMembers, Profile
from datetime import datetime,date, timedelta
from django.contrib.auth.models import User
from calendar import HTMLCalendar
from group.models import *
from calendar_app.forms import SigninForm, EventForm
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from datetime import datetime
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.contrib import messages
from .calendar import Calendar
from calendar_pro.views import *
import calendar
# Create your views here.



def current_date(current):
     if current:
         year, month = current.split('-')
         return datetime(year = int(year), month = int(month), day = 1)
     return datetime.today()

def Next(day):
    total_days = calendar.monthrange(day.year,day.month)[1]
    day = day.replace(day = total_days)
    # day -> object of datetime, can u add something on any object + 1, istead of this, you can do -> object + object
    # timedelta is basically used for doing Arithmetic operation in datetime object
    next_month = day + timedelta(days=1)
    print("next-month",next_month)
    
    month_year ="month_year=" + str(next_month.year) + '-' + str(next_month.month)
    print(month_year)
    return month_year

def Previous(day):
    day = day.replace(day = 1)
    previous_month = day - timedelta(days=1)
    month_year = "month_year=" + str(previous_month.year) + '-' + str(previous_month.month)
    return month_year

def get_context_data(request):
    current = current_date(request.GET.get("month_year",None))
    print("current-month",current)
   
    html = Calendar(current.year, current.month)
    html_cal = html.Active_day()
    
    current_month_events = Event.objects.filter(start_at__month = current.month)
    events = []
    for event in Member_or_Not(request.user):
        for current_mon_ev in current_month_events:
               if event.start_at == current_mon_ev.start_at:
                      events.append(event)

    content = {
    'next' : Next(current), #month_year=2022-8
    'previous' :Previous(current),
    'calendar' : format_html(html_cal),
    'events' : events,
    'list' : Group_Mem(request.user),
    'today' : datetime.today(),
    'current_month_events' : current_month_events,
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    return content


@login_required
def Eventdisplay(request):
    print(request.GET)
    context = get_context_data(request)
    return render(request, 'calendar_app/eventlist.html', context)


# // Here above, the format_html or mark_safe are same kind of method which makes the format as it is
# // like here if we not use the format_html(html_cal) then in web page the it shows the content in html_cal
# not the output view (as html_cal here is a html code in text format so to use it in web we have to use format_html or mark_safe)

@login_required
def CreateEvent(request):
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            creator = request.user
            title = form.cleaned_data['title']
            about = form.cleaned_data['about']
            start_at = form.cleaned_data['start_at']
            end_at = form.cleaned_data['end_at']
            about = form.cleaned_data['about']
            obj = Event(creator = creator,title = title, start_at = start_at, end_at = end_at, about = about)
            obj.save()
            messages.success(request, "Your event has successfully created!")
            EventMembers.objects.create(event = obj, member = request.user )
            return redirect(obj)
    context = {
    'form' : form,
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    return render(request, 'calendar_app/event_form.html',context)

def EventInfo(request,pk):
    event = get_object_or_404(Event, pk = pk)
    members = EventMembers.objects.filter(event = event)
    context = {
    'event' : event,
    'members' : members,
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    return render(request, 'calendar_app/event_detail.html', context)

def UpdateEvent(request, pk):
    event = Event.objects.get(id = pk)
    if request.user == event.creator:
        event_form = EventForm(instance = event)
        if request.method == 'POST':
            event_form = EventForm(request.POST, instance = event)
            if event_form.is_valid():
                 event_form.save()
                 messages.success(request, "Your event is updated successfully!")
                 return redirect(Event.objects.get(id=pk))
        return render(request, 'calendar_app/update_event.html', {'form' : event_form , 'events' : Event.objects.all()})
    else:
        messages.warning(request, f"You are not the creator of : {event.title} event so you can't update!")
    context = {
    'event' : event,
    'members' : EventMembers.objects.filter(event = event),
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    return render(request, 'calendar_app/event_detail.html', context)


def DeleteEvent(request, pk):

    event = get_object_or_404(Event, pk = pk)
    if request.user == event.creator:
        event.delete()
        messages.success(request, "You have deleted this event successfully!")
        return redirect('/')
    else:
        messages.success(request, f"You are not the creator of : {event.title} event, so you can't delete!")

    return redirect('/')

# /////////////////////// EventMembers /////////////////////////

def JoinEvent(request, pk):
    event = get_object_or_404(Event, id = pk)
    eventmember = EventMembers(event = event, member = request.user)
    if Event.objects.get(id = pk).creator == request.user:
        messages.warning(request, "Since you are the creator of this event so you are already the member of this group!")
    try:
        eventmember.save()
        messages.success(request, 'You successfully joined this event!')
    except:
        pass
    context = {
    'event' : event,
    'members' : EventMembers.objects.filter(event = event),
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    return render(request,'calendar_app/event_detail.html',context)

def LeaveEvent(request, pk):
    event = get_object_or_404(Event, id = pk)
    eventmember = EventMembers.objects.filter(event = event, member = request.user)
    # // Mind it the queryset is always in the form of iterator
    # // so we are doing this to get that particular objects which is going to leave this event
    try:
       if Event.objects.get(id = pk).creator == request.user:
            messages.warning(request, "You can't leave this event as you are the creator, You have to delete this event instead!")
       elif request.user == eventmember[0].member:
            eventmember.delete()
            messages.success(request, 'You leaved this event successfully!')
    except:
        pass

    context = {
    'event' : event,
    'members' : EventMembers.objects.filter(event = event),
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    return render(request, 'calendar_app/event_detail.html', context)

def Kick_out(request,event_pk,pk):
    event = Event.objects.get(id=event_pk)
    if event.creator.username == request.user.username:
        if request.user.username == User.objects.get(id=pk).username:
            messages.warning(request, "Since you are the creator so you can't kick Yourself out, instead you have to delete this event!")
        else:
            kick_me = EventMembers.objects.filter(event__id = event_pk, member__id = pk )
            kicked_to = kick_me[0].member.username
            kick_me.delete()
            messages.warning(request, f"You have successfully kicked {kicked_to}")
    else:
        messages.warning(request, "You are not the creator of this event so you can't kick_out the member")
    context = {
    'event' : get_object_or_404(Event, pk = event_pk),
    'members' : EventMembers.objects.filter(event__id=event_pk),
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    return render(request,'calendar_app/event_detail.html', context)


# ///////////////////////////// Members Profile ///////////////////////////////////////////////

def Memberprofile(request, pk):
    instant_user =  User.objects.get(id=pk)
    # instant_profile = Profile.objects.get(id = instant_user.id)
                                                                # ////Since i have to grab Profile of the user so i have to do
                                                                # /// Profile.objects.get(user_name = instant_user.id) not
                                                                # ///Profile.objects.get(id = instant_user.id)
    member_profile = Profile.objects.get(user_name = instant_user.id)
                                                                # ///Now here we have filter method to get all the event related to that mamber
                                                                # ///If we use get instead of filter then mind it get only gives you a single object
    active_events = Event.objects.filter(creator = instant_user.id)
    context = {
    'member_pro' : member_profile,
    'memberevents' : active_events,
    'instant_user' : instant_user,
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    return render(request, 'calendar_app/memberprofile.html', context)




















#
