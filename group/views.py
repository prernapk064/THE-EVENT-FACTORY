from django.shortcuts import render, get_object_or_404, redirect
from .models import Group
from django.contrib import messages
from .forms import *
from calendar_pro.views import *
# Create your views here.

def GroupList(request):
     context = {
        'events' : Member_or_Not(request.user),
        'list' : Group_Mem(request.user)     }
     return render(request, 'group/grouplist.html', context)

def GroupDetail(request, pk):
    group = get_object_or_404(Group, pk = pk)
    context = {
    'group' : group,
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'members' : GroupMembers.objects.filter(group = group),
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    return render(request, 'group/groupdetail.html', context)

def CreateGroup(request):
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data["group_name"]
            about = form.cleaned_data['about']
            creator = request.user
            group = Group.objects.create(group_name = group_name, creator = creator, about = about)
            messages.success(request, "Your group has created successfully!")
            GroupMembers.objects.create(group = group, member_name = request.user)
            return render(request, 'group/groupdetail.html', {'group' : group,
                                                              'event' : Member_or_Not(request.user),
                                                              'list' : Group_Mem(request.user),
                                                              'members' : GroupMembers.objects.filter(group = group),
                                                              'all_ev' : AllEvents("give"),
                                                              'all_gr' : AllGroups("give")})
    context = {
        'form' : form,
        'events' : Member_or_Not(request.user),
        'list' : Group_Mem(request.user),
        'all_ev' : AllEvents("give"),
        'all_gr' : AllGroups("give")
        }
    return render(request, 'group/creategroup.html', context)

def UpdateGroup(request, pk):
    group = get_object_or_404(Group, pk = pk)
    form = GroupForm(instance = group)
    if request.user == group.creator:
        if request.method == "POST":
            form = GroupForm(request.POST, instance = group)
            if form.is_valid():
                form.save()
                messages.success(request, "Your group has updated successfully!")
                return redirect(group)
    else:
        messages.warning(request, "You can't update this group!")
        return redirect('/')
    context = {
        'form' : form,
        'events' : Member_or_Not(request.user),
        'list' : Group_Mem(request.user),
        'all_ev' : AllEvents("give"),
        'all_gr' : AllGroups("give")
        }
    return render(request, 'group/updategroup.html', context)



def DeleteGroup(request,pk):
    group = get_object_or_404(Group, pk = pk)
    if request.user == group.creator:
        group.delete()
        messages.success(request, "Group has been deleted successfully!")
    else:
        messages.warning(request, "You are not the creator of this group so you can't delete it!")
    return redirect('calendar_app:eventlist')


def JoinGroup(request, pk):
    group = Group.objects.get(id = pk)
    if request.user != group.creator:
       try:
           if GroupMembers.objects.get(group = group, member_name = request.user):
               messages.success(request, "You are already the member of this group!")
       except:
              GroupMembers.objects.create(group = group, member_name = request.user)
              messages.success(request, "You have joined the group successfully!")
    else:
        messages.warning(request, "Since you are the creator of this group!")
    context = {
    'group' : group,
    'members' : GroupMembers.objects.filter(group = group),
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    return render(request, 'group/groupdetail.html', context)


def LeaveGroup(request, pk):
    group = Group.objects.get(id = pk)
    if request.user != group.creator:
        groupmember = GroupMembers.objects.get(group = group, member_name = request.user)
        if groupmember in GroupMembers.objects.all():
             groupmember.delete()
             messages.success(request, "You have leaved this group successfully!")
    else:
        messages.warning(request, "Since you are the creator of this group so only you can delete the group instead of leaving the group!")
    context = {
    'group' : group,
    'members' : GroupMembers.objects.filter(group = group),
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    return render(request, "group/groupdetail.html", context)

def Kick_out(request,group_pk,pk):
    group = Group.objects.get(id=group_pk)
    if group.creator.username == request.user.username:
        if request.user.username == User.objects.get(id=pk).username:
            messages.warning(request, "Since you are the creator so you can't kick Yourself out, instead you have to delete this event!")
        else:
            kick_me = GroupMembers.objects.filter(group__id = group_pk, member_name__id = pk )
            kicked_to = kick_me[0].member_name.username
            kick_me.delete()
            messages.warning(request, f"You have successfully kicked {kicked_to}")
    else:
        messages.warning(request, "You are not the creator of this event so you can't kick_out the member")
    context = {
    'group' : get_object_or_404(Group, pk = group_pk),
    'members' : GroupMembers.objects.filter(group__id=group_pk),
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    return render(request,'group/groupdetail.html', context)

