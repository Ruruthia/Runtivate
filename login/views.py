from django.contrib.auth import login, authenticate
from django.http import Http404
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

from .models import Profile, Activity
from .forms import NameForm, ActivityForm


def home_view(request):

    """Home view. When user is logged in but does not have a profile it requests making one."""
    if request.user.is_authenticated and not hasattr(request.user, 'profile'):
        return redirect('/form')
    else:
        return render(request, 'home.html')


def signup(request):

    """View used for signing up."""
    message = "Sign up!"
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
    return render(request, 'signup.html', {'form': form, 'message': message})


def form_view(request):

    """View used for creating a profile."""
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = NameForm(request.POST)
            if form.is_valid():
                request.user.profile = Profile()
                request.user.profile.weight = form.cleaned_data['weight']
                request.user.profile.height = form.cleaned_data['height']
                request.user.profile.age = form.cleaned_data['age']
                request.user.profile.gender = form.cleaned_data['gender']
                request.user.profile.save()
                return redirect('/')
        else:
            form = NameForm()
        return render(request, 'form.html', {'form': form})
    else:
        return render(request, 'home.html')


def data_view(request):

    """View used for showing information about user's profile."""
    if request.user.is_authenticated:
        return render(request, 'data.html')
    else:
        return redirect('home')


def update_view(request):

    """View used for updating user's profile."""
    message = "Update your account!"
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = NameForm(request.POST)
            if form.is_valid():
                request.user.profile.weight = form.cleaned_data['weight']
                request.user.profile.height = form.cleaned_data['height']
                request.user.profile.age = form.cleaned_data['age']
                request.user.profile.gender = form.cleaned_data['gender']
                request.user.profile.save()
                return redirect('data/')
        else:
            form = NameForm(initial={"weight": request.user.profile.weight, 'height': request.user.profile.height,
                                     'age': request.user.profile.age, 'gender': request.user.profile.gender})
        return render(request, 'form.html', {'form': form, 'message': message})
    else:
        return redirect('home')


def add_activity(request):

    """View used for adding new activity."""
    message = "Add new activity!"
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ActivityForm(request.POST)
            if form.is_valid():
                new_activity = Activity()
                new_activity.profile = request.user.profile
                new_activity.date = form.cleaned_data['date']
                new_activity.distance = form.cleaned_data['distance']
                new_activity.duration = form.cleaned_data['duration']
                new_activity.comment = form.cleaned_data['comment']
                new_activity.save()
                return redirect('view_history')
        else:
            form = ActivityForm()
        return render(request, 'form.html', {'form': form, 'message': message})
    else:
        return redirect('home')


def history_view(request):

    """View used for showing history of user's activities."""
    if request.user.is_authenticated:
        history = Activity.objects.all().filter(profile=request.user.profile, date__lte=timezone.now()).order_by(
            '-date')
        contex = {'history': history}
        return render(request, 'history.html', contex)
    else:
        return redirect('home')


def activity_detail_view(request, activity_id):

    """View used for showing details of one activity."""
    if request.user.is_authenticated:
        activity = get_object_or_404(Activity, pk=activity_id)
        if activity.profile.id is not request.user.profile.id:
            raise Http404("Activity does not exist")
        calories = round(activity.distance * request.user.profile.weight * 1.036)
        tempo = round(activity.duration / activity.distance, 2)
        return render(request, 'details.html', {'activity': activity, 'calories': calories, 'tempo': tempo})
    else:
        return redirect('home')


def remove_view(request, activity_id):

    """View used for showing that activity has been deleted."""
    if request.user.is_authenticated:
        activity = get_object_or_404(Activity, pk=activity_id)
        if activity.profile.id is not request.user.profile.id:
            raise Http404("Activity does not exist")
        activity.delete()
        return render(request, 'deleted.html')
    else:
        return redirect('home')


def edit_activity(request, activity_id):

    """View used for editing an activity."""
    message = "Edit this activity!"
    if request.user.is_authenticated:
        activity = get_object_or_404(Activity, pk=activity_id)
        if activity.profile.id is not request.user.profile.id:
            raise Http404("Activity does not exist")
        if request.method == 'POST':
            form = ActivityForm(request.POST)
            if form.is_valid():
                activity.date = form.cleaned_data['date']
                activity.distance = form.cleaned_data['distance']
                activity.duration = form.cleaned_data['duration']
                activity.comment = form.cleaned_data['comment']
                activity.save()
                return redirect('/view_history')
        else:
            form = ActivityForm(
                initial={'date': activity.date, 'distance': activity.distance, 'duration': activity.duration,
                         'comment': activity.comment})
        return render(request, 'form.html', {'form': form, 'message': message})
    else:
        return redirect('home')


def stats_view(request):

    """View used for showing statistics of user's activities."""
    if request.user.is_authenticated:
        activities = Activity.objects.all().filter(profile=request.user.profile, date__lte=timezone.now())
        if not activities:
            return render(request, 'stats.html')
        count = activities.count()
        calories = 0
        distance = 0
        time = 0
        for activity in activities:
            calories += round(activity.distance * request.user.profile.weight * 1.036)
            distance += activity.distance
            time += activity.duration
        avg_tempo = round(time / distance, 2)
        return render(request, 'stats.html', {'count': count, 'calories': calories, 'distance': distance, 'time': time,
                                              'avg_tempo': avg_tempo})
    else:
        return redirect('home')
