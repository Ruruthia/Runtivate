"""mysite URL Configuration

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
from login.views import home_view, form_view, data_view, update_view, add_activity, history_view, activity_detail_view, remove_view, edit_activity
from django.conf.urls import url
from login import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    url(r'^signup/$', core_views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    url('form/', form_view),
    url('data/', data_view, name='data_page'),
    url('update/', update_view, name='update'),
    url('new_activity/', add_activity, name='add_activity'),
    path('view_history/', history_view, name='view_history'),
    path('view_history/<int:activity_id>/', activity_detail_view, name='detail'),
    path('remove/<int:activity_id>', remove_view, name='remove'),
    path('edit/<int:activity_id>', edit_activity, name='edit'),
]