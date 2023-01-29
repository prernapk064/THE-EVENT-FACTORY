from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.contrib.auth.models import User
from calendar_app.models import Event
from calendar_app.forms import ProfileForm
from calendar_app.models import Profile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from group.models import *
from post_app.models import Post


def AllEvents(*args):
    return Event.objects.all()

def AllGroups(*args):
    return Group.objects.all()

def VisitEvent(request, pk):
    event_details = Event.objects.get(id = pk)
    all_posts = Post.objects.filter(event = event_details)
    members = EventMembers.objects.filter(event = event_details)
    context = {
    'eve' : event_details,
    'all_posts' : all_posts,
    'members' : members,
    }
    return render(request, 'visitevent.html', context)

# /// Particular person's events //////
def Member_or_Not(user):
    events = []
    for event in Event.objects.all():
        for mem in EventMembers.objects.filter(event = event):
            if mem.member == user:
                events.append(event)
    return events

# // Particular person's Groups ////
def Group_Mem(user):
    groups = []
    for group in Group.objects.all():
        for mem in GroupMembers.objects.filter(group = group):
            if user == mem.member_name:
                groups.append(group)
    return groups


def Home(request):
    # // get() return an object
    context = {
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'visit_events' : Event.objects.all(),
    'can_see_event' : "go",
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    return render(request, 'home.html', context)

class ThanksView(TemplateView):
    template_name = 'thanks.html'

def Index(request):
    list = Group.objects.all()
    context = {
       'events' : Member_or_Not(request.user),
       'list' : Group_Mem(request.user),
       'visit_events' : Event.objects.all(),
       'all_ev' : AllEvents("give"),
       'all_gr' : AllGroups("give")
       }
    return render(request, 'guidance.html', context)

# ///////////////////////// Profile //////////////////////////////////////////
@login_required
def ProfileinfoView(request):

    context = {
    'profile' : Profile.objects.get(user_name = request.user),
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    return render(request, 'profiledetail.html', context)


@login_required
def UpdateProfile(request):
    profile = Profile.objects.get(user_name = request.user)
    profileform = ProfileForm(instance = profile)
    if request.method == 'POST':
        profileform = ProfileForm(request.POST,request.FILES,instance = profile )
        if profileform.is_valid():
            profileform.save()
            messages.success(request, "You have updated your profile successfully")
            return redirect('profiledetail')
    context = {
             'form' : profileform,
             'events' : Member_or_Not(request.user),
             'list' : Group_Mem(request.user),
             'all_ev' : AllEvents("give"),
             'all_gr' : AllGroups("give")
    }
    return render(request, 'updateprofile.html', context)

