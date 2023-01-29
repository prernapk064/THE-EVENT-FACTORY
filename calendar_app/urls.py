from django.urls import path
from django.contrib.auth import views as auth_views
from . import signup
from . import views

app_name = 'calendar_app'


urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name = 'calendar_app/login.html'),name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(),name = 'logout'),
    path('signin/',signup.Signin,name = 'signin'),
    path('',views.Eventdisplay,name = 'eventlist'),
    path('createevent/',views.CreateEvent, name = "createevent"),
    path('eventdetail/<int:pk>/',views.EventInfo, name='eventinfo'),
    path('updateevent/<int:pk>/', views.UpdateEvent, name = 'updateevent'),
    path('delete_event/<int:pk>/', views.DeleteEvent, name = 'deleteevent'),
    path('joinevent/<int:pk>/', views.JoinEvent, name = 'joinevent'),
    path('leaveevent/<int:pk>/', views.LeaveEvent, name = 'leaveevent'),
    path('kick_out/<int:event_pk>/<int:pk>/', views.Kick_out, name = 'kick_out'),
    path('memberprofile/<int:pk>/', views.Memberprofile, name = 'memberprofile'), 
    
]
