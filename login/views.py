from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Profile
from .forms import NameForm
from django.http import HttpResponseRedirect

def home_view(request):

    if request.user.is_authenticated and not hasattr(request.user, 'profile'):
        return redirect('/form')
    else: return render(request, 'home.html')

def form_view(request):

    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            request.user.profile = Profile()
            request.user.profile.weight = form.cleaned_data['weight']
            request.user.profile.height=form.cleaned_data['height']
            request.user.profile.age=form.cleaned_data['age']
            request.user.profile.gender=form.cleaned_data['gender']


            request.user.profile.save()
            return redirect('/')
    else:
        form = NameForm()
    return render(request, 'login/form.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'login/signup.html', {'form': form})


