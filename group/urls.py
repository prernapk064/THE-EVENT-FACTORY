from django.urls import path
from . import views

app_name = 'group'

urlpatterns = [
     path('groupdetail/<int:pk>/', views.GroupDetail, name = 'groupdetail'),
     path('creategroup/', views.CreateGroup, name ='creategroup'),
     path('updategroup/<int:pk>/', views.UpdateGroup, name = 'updategroup'),
     path('deletegroup/<int:pk>/', views.DeleteGroup, name = 'deletegroup'),
     path('joingroup/<int:pk>/', views.JoinGroup, name = 'joingroup'),
     path('leavegroup/<int:pk>/', views.LeaveGroup, name = 'leavegroup'),
     path('kick_out/<int:group_pk>/<int:pk>/', views.Kick_out, name = 'kick_out')
]
