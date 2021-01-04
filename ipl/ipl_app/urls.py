"""ipl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from ipl_app.views import *
from django.http import HttpResponseRedirect
urlpatterns = [
    path('', home_view, name="home_html"),
    path('season/<int:season>/', season_view, name="season_html"),
    path('season/', season_view, name="season_home"),
    path('pointstable/<int:season>/', points_view, name="points_html"),
    path('pointstable/', points_home, name="points_home"),
    path('season/<int:season>/match/<int:mid>', match_view, name="match_html"),

    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView, name="logout"),
    path('details/', details_view, name="details"),

    path('team/<str:team>/', team_view, name="team_html"),
    path('ipl_admin/', admin_view, name="admin_html"),
]

