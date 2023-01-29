from django.urls import path
from . import views

app_name = 'post_app'


# // Remember the pk defined here for "post" is not a pk for the post, it is for
# the particular event's pk for that post

urlpatterns = [
    path('<int:pk>/', views.PostView, name='post'),
    path('createpost/<int:pk>', views.CreatePost, name="createpost"),
    path('updatepost/<int:pk>/', views.UpdatePost, name='updatepost'),
    path('deletepost/<int:pk>/', views.DeletePost, name='deletepost'),
]
