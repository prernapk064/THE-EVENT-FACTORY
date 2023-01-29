from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from calendar_app.models import Event, EventMembers
from django.contrib import messages
from .models import Post
from .forms import PostForm
from group.models import *
from calendar_pro.views import *
# Create your views here.


@login_required
def PostView(request, pk):
    event = Event.objects.get(id = pk)
    posts = Post.objects.filter(event = event)
    context = {
    'event' : event,
    'posts' : posts,
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    return render(request, 'post_app/post.html', context)

@login_required
def CreatePost(request, pk):
    form = PostForm()
    context = {
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'form' : form,
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
    }
    if request.method == "POST":
        form  = PostForm(request.POST)
        if form.is_valid():
            post = form.cleaned_data['post']
            event = Event.objects.get(id = pk)
            post_obj = Post.objects.create(post = post, event = event)
            messages.success(request, f"You have created a post for {event.title} event")
            return redirect(post_obj)
            # In redirect we can either pass the  objects(as redirect search the get_absolute_url of that object),
            # or we can pass the view along with the kwargs or we can directly pass the url path as well
    return render(request, 'post_app/create_post.html', context)


@login_required
def UpdatePost(request, pk):
    event = Post.objects.get(id=pk).event
    event_members = EventMembers.objects.filter(event = event)
    posts = Post.objects.filter(event = event)
    post = Post.objects.get(id=pk)
    form = PostForm(instance = post)
    # // Here the one can only update who is the memeber of this Post's event //
    # // Now here event_members are a queryset so it is iterable so each element is a EventMembers objects //
    # // thus we can check if the user is a member of this event or not
    context = {
    'events' : Member_or_Not(request.user),
    'list' : Group_Mem(request.user),
    'event' : event,
    'posts' : posts,
    'form' : form,
    'all_ev' : AllEvents("give"),
    'all_gr' : AllGroups("give")
        }
    if request.user in [each_obj.member for each_obj in event_members]:
        if request.method == "POST":
            form = PostForm(request.POST, instance = post)
            if form.is_valid():
                form.save()
                messages.success(request, "You have updated the post successfully!")
                return render(request, 'post_app/post.html', context)
    else:
            messages.success(request, "You are not the member of this Event so you can't update!")
            return render(request, 'post_app/post.html', context)
    return render(request, 'post_app/updatepost.html',context)


@login_required
def DeletePost(request, pk):
    post = Post.objects.get(id = pk)
    event = post.event
    posts = Post.objects.filter(event = event)
    event_members = EventMembers.objects.filter(event = event)
    context = {
        'event' : event,
        'posts' : posts,
        'events' : Member_or_Not(request.user),
        'list' : Group_Mem(request.user),
        'all_ev' : AllEvents("give"),
        'all_gr' : AllGroups("give")
        }
    if request.user in [each_obj.member for each_obj in event_members]:
        post.delete()
        messages.success(request, "You have deleted the post successfully!")
        return redirect('/')
    else:
        messages.success(request, "You are not a part of this event so you can't delete!")

    return render(request, 'post_app/post.html', context)
