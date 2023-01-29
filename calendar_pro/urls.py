"""calendar_pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import ProfileinfoView
from django.contrib.auth import views as auth_views
from . import views
from calendar_app import signup

urlpatterns = [
    path('',views.Home,name = 'HOME'),
    path('index/',views.Index,name = 'view'),
    path('visitevent/<int:pk>/', views.VisitEvent, name = 'visitevent'),
    #use of as_view() only when you are using any class in views.py else use it normally
    path('thanks/',views.ThanksView.as_view(),name = 'THANKS'),
    path('admin/', admin.site.urls),
    path('profiledetail/', views.ProfileinfoView, name = 'profiledetail'),
    path('calendar_app/',include('calendar_app.urls',namespace='calendar_app')),
    path('post_app/', include('post_app.urls', namespace='post_app')),
    path('group/', include('group.urls', namespace='group')),
    path('updateprofile/', views.UpdateProfile, name = 'updateprofile'),
    path('passwordreset/', auth_views.PasswordResetView.as_view(template_name = 'passwordreset.html'), name = 'password_reset'),
    path('passwordreset_done/', auth_views.PasswordResetDoneView.as_view(template_name = 'passwordreset_done.html'), name = 'password_reset_done'),
    path('passwordreset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'passwordreset_confirm.html'), name = 'password_reset_confirm'),
    path('passwordreset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'passwordreset_complete.html'), name = 'password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
