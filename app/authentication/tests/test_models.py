from datetime import datetime
from django.test import TestCase
from unittest import mock
from django.utils import dateparse

from app.authentication.models import User


class UserModelTest(TestCase):
    def test_values(self):
        '''This function creates a test case user with all values'''
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = dateparse.parse_datetime("2022-06-11T10:30:00Z")
            user = User.objects.create(
                username = 'tembo',
                email = 'tembo@gmail.com',
            )

        self.assertEqual(user.email, 'tembo@gmail.com')
        self.assertIsNot(user.username, 'tembo1')
        self.assertEqual(user.is_active, False)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_verified)


    def test_errors(self):
        '''This function tests the errors'''
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = dateparse.parse_datetime("2022-06-11T10:30:00Z")
            user = User.objects.create(
                username = 'tembo',
                email = 'tembo@gmail.com',
            )
        self.assertRaises(ValueError)


    def test_is_active(self):
        '''Tests if user is active'''
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = dateparse.parse_datetime("2022-06-11T10:30:00Z")
            user = User.objects.create(
                username = 'tembo',
                email = 'tembo@gmail.com',
                is_active = True
            )

        self.assertEqual(user.email, 'tembo@gmail.com')
        self.assertIsNot(user.username, 'tembo1')
        self.assertEqual(user.is_active, True)


    def test_is_staff(self):
        '''Tests if the user is staff'''
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = dateparse.parse_datetime("2022-06-11T10:30:00Z")
            user = User.objects.create(
                username = 'tembo',
                email = 'tembo@gmail.com',
                is_staff = True
            )

        self.assertEqual(user.is_staff, True)
        self.assertTrue(user.is_staff)


    def test_is_verified(self):
        '''Tests if user is verified'''
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = dateparse.parse_datetime("2022-06-11T10:30:00Z")
            user = User.objects.create(
                username = 'tembo',
                email = 'tembo@gmail.com',
                is_verified = True
            )

        self.assertIsNot(user.is_verified, False)
        self.assertTrue(user.is_verified)







    # def test_is_active(self):
    #     with mock.patch('django.utils.timezone.now') as mock_now:
    #         mock_now.return_value = dateparse.parse_datetime("2022-06-13T09:00z")
    #         user = User.objects.create(
    #             username = 'tembo',
    #             email = 'tembo@gmail.com',
    #             is_active = True
    #         )

    #     self.assertTrue(user.is_active)