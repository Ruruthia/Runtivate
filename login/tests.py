import datetime

from django.test import TestCase, Client
from django.urls import reverse

from .models import Profile, Activity, User
from .forms import NameForm, ActivityForm


def create_activity(user, date, duration, distance, comment):
    return Activity.objects.create(profile=user.profile, date=date, duration=duration,
                                   distance=distance, comment=comment)


class HistoryViewTests(TestCase):

    def set_up(self):
        """Sets up user for tests. Run before every other test."""
        self.client = Client()
        self.user = User.objects.create_user('foo', 'myemail@test.com', 'bar')
        self.logged_in = self.client.login(username='foo', password='bar')
        self.user.profile = Profile.objects.create(user=self.user, weight=40, height=140, age=20, gender="F")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.logged_in, 1)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.all().first(), User.objects.all().first().profile)

    def test_no_activities(self):
        """If no activities exist, proper message is displayed."""
        self.set_up()
        response = self.client.get(reverse('view_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No activities are available!")
        self.assertQuerysetEqual(
            response.context['history'],
            []
        )

    def test_past_activity(self):
        """Past activity is displayed on history page."""
        self.set_up()
        create_activity(self.user, datetime.datetime.now() - datetime.timedelta(days=5), 1, 1, "Past")
        response = self.client.get(reverse('view_history'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['history'],
            ['<Activity: Past>']
        )

    def test_future_activity(self):
        """Future activity is not displayed on history page. """
        self.set_up()
        create_activity(self.user, datetime.datetime.now() + datetime.timedelta(days=5), 1, 1, "Future")
        response = self.client.get(reverse('view_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No activities are available!")
        self.assertQuerysetEqual(
            response.context['history'],
            []
        )

    def test_future_and_past_activity(self):
        """When past and future activities are created, only past ones are displayed on history page."""
        self.set_up()
        create_activity(self.user, datetime.datetime.now() + datetime.timedelta(days=5), 1, 1, "Future")
        create_activity(self.user, datetime.datetime.now() - datetime.timedelta(days=5), 1, 1, "Past")
        response = self.client.get(reverse('view_history'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['history'],
            ['<Activity: Past>']
        )

    def test_two_past_activities(self):
        """History page can display more than one past activity."""
        self.set_up()
        create_activity(self.user, datetime.datetime.now() - datetime.timedelta(days=5), 1, 1, "Past 1")
        create_activity(self.user, datetime.datetime.now() - datetime.timedelta(days=5), 1, 1, "Past 2")
        response = self.client.get(reverse('view_history'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['history'],
            ['<Activity: Past 1>', '<Activity: Past 2>', ]
        )


class StatsViewTests(TestCase):

    def set_up(self):
        """Sets up user for tests. Run before every other test."""
        self.client = Client()
        self.user = User.objects.create_user('foo', 'myemail@test.com', 'bar')
        self.logged_in = self.client.login(username='foo', password='bar')
        self.user.profile = Profile.objects.create(user=self.user, weight=40, height=140, age=20, gender="F")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.logged_in, 1)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.all().first(), User.objects.all().first().profile)

    def test_no_activities(self):
        """If no activities exist, proper message is displayed."""
        self.set_up()
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add some past activities first!")

    def test_past_activity(self):
        """Stats are based on past activity."""
        self.set_up()
        create_activity(self.user, datetime.datetime.now() - datetime.timedelta(days=5), 60, 10, "Past")
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Number of activites: 1")
        self.assertContains(response, "Distance: 10.0")
        self.assertContains(response, "Average tempo: 6.0")

    def test_future_activity(self):
        """Future activity does not affect stats."""
        self.set_up()
        create_activity(self.user, datetime.datetime.now() + datetime.timedelta(days=5), 1, 1, "Future")
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add some past activities first!")

    def test_future_and_past_activity(self):
        """When both past and future activities exist, stats are based only on past one."""
        self.set_up()
        create_activity(self.user, datetime.datetime.now() - datetime.timedelta(days=5), 60, 10, "Past")
        create_activity(self.user, datetime.datetime.now() + datetime.timedelta(days=5), 1, 1, "Future")
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Number of activites: 1")
        self.assertContains(response, "Distance: 10.0")
        self.assertContains(response, "Average tempo: 6.0")

    def test_two_past_activities(self):
        """Stats take into consideration multiple past activities."""
        self.set_up()
        create_activity(self.user, datetime.datetime.now() - datetime.timedelta(days=5), 60, 10, "Past 1")
        create_activity(self.user, datetime.datetime.now() - datetime.timedelta(days=5), 30, 8, "Past 2")
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Number of activites: 2")
        self.assertContains(response, "Distance: 18.0")
        self.assertContains(response, "Average tempo: 5.0")


class ProfileFormTests(TestCase):

    def set_up(self):
        """Sets up user for tests. Run before every other test."""
        self.client = Client()
        self.user = User.objects.create_user('foo', 'myemail@test.com', 'bar')
        self.logged_in = self.client.login(username='foo', password='bar')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.logged_in, 1)

    def test_valid_form(self):
        """Form is valid when weight, height, age and gender are valid."""
        self.set_up()
        data = {'weight': 40, 'height': 140, 'age': 20, 'gender': "Female"}
        form1 = NameForm(data=data)
        data = {'weight': 60, 'height': 180, 'age': 50, 'gender': "Male"}
        form2 = NameForm(data=data)
        self.assertTrue(form1.is_valid())
        self.assertTrue(form2.is_valid())

    def test_invalid_blank_form(self):
        """ Form is invalid when values are blank."""
        self.set_up()
        data = {'weight': '', 'height': '', 'age': '', 'gender': ''}
        form = NameForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_with_invalid_types(self):
        """From is invalid when values have wrong types"""
        self.set_up()
        data = {'weight': 'test_weight', 'height': 'test_height', 'age': 'test_age', 'gender': 'test_gender'}
        form = NameForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_with_invalid_values(self):
        """Form is invalid when values are too small."""
        self.set_up()
        data = {'weight': 5, 'height': 5, 'age': 10, 'gender': "Female"}
        form = NameForm(data=data)
        self.assertFalse(form.is_valid())


class ActivityFormTests(TestCase):

    def test_valid_form_with_comment(self):
        """Form is valid when date, duration and distance values are valid. Comment is not required."""
        data = {'date': datetime.datetime.now(), 'duration': 1, 'distance': 1, 'comment': 'text_comment'}
        form = ActivityForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_form_without_comment(self):
        """Form is valid also when comment is not provided."""
        data = {'date': datetime.datetime.now(), 'duration': 1, 'distance': 1}
        form = ActivityForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_blank_form(self):
        """ Form is invalid when values are blank."""
        data = {'date': '', 'duration': '', 'distance': ''}
        form = ActivityForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_with_invalid_types(self):
        """From is invalid when values have wrong types"""
        data = {'date': 'test_date', 'duration': 'test_duration', 'distance': 'test_distance'}
        form = ActivityForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_with_invalid_values(self):
        """Form is invalid when duration and/or distance are negative."""
        data = {'date': datetime.datetime.now(), 'duration': -1, 'distance': -1}
        form = ActivityForm(data=data)
        self.assertFalse(form.is_valid())


class RedirectionTests(TestCase):

    def set_up(self):
        """Sets up user for tests. Run before every other test."""
        self.client = Client()
        self.user = User.objects.create_user('foo', 'myemail@test.com', 'bar')
        self.assertEqual(User.objects.count(), 1)

    def test_not_logged(self):
        """If user is not logged in, redirect every other page to home."""
        self.set_up()
        response = self.client.get('/stats/', follow=True)
        self.assertRedirects(response, '/')

    def test_has_no_profile(self):
        """If user is logged in and does not have profile, redirect to form to create one."""
        self.set_up()
        self.client.login(username='foo', password='bar')
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/form/')
