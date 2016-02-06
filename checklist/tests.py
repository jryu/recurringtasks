import json

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase

from .models import Check, Task

class MainViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.the_user = User.objects.create_user(username='u', password='p')

    def setUp(self):
        self.client.force_login(self.the_user)

    def test_new_task_sort_order(self):
        new_task = Task.objects.create(
                name='new_task', interval='10', created_by=self.the_user)
        other_task = Task.objects.create(
		name='other_task', interval='10', created_by=self.the_user)

        Check.objects.create(task=other_task, date='2016-01-15')

        response = self.client.get(reverse('main'))
        tasks = response.context['object_list']
        self.assertEqual(tasks.count(), 2)
        self.assertEqual(tasks[0].name, "new_task")

    def test_last_date_sort_order(self):
        task1 = Task.objects.create(
                name='1', interval='10', created_by=self.the_user)
        task2 = Task.objects.create(
		name='2', interval='10', created_by=self.the_user)

        Check.objects.create(task=task1, date='2016-01-15')
        Check.objects.create(task=task2, date='2016-01-16')
        Check.objects.create(task=task1, date='2016-01-17')

        response = self.client.get(reverse('main'))
        tasks = response.context['object_list']
        self.assertEqual(tasks.count(), 2)
        self.assertEqual(tasks[0].name, "2")


class CheckTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.the_user = User.objects.create_user(username='u', password='p')
        cls.task = Task.objects.create(
                name='testing', interval='10', created_by=cls.the_user)

    def setUp(self):
        self.client.force_login(self.the_user)

    def test_date_in_response(self):
        response = self.client.post(reverse('check'), {
            'task': self.task.pk,
            'date': '1/15/2016'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content.decode('utf-8'))
        data.pop('pk', None)
        self.assertEqual(data, {
            'year': 2016,
            'month': 1,
            'day': 15
        })

        self.assertEqual(Check.objects.count(), 1)

    def test_invalid_task(self):
        # Set invalid task value
        response = self.client.post(reverse('check'), {
            'task': self.task.pk + 1,
            'date': '1/15/2016'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 400)
        self.assertTrue('task' in response.json())
        self.assertEqual(Check.objects.count(), 0)

    def test_other_user(self):
        self.client.force_login(
                User.objects.create_user(username='other_user', password='p'))

        response = self.client.post(reverse('check'), {
            'task': self.task.pk,
            'date': '1/15/2016'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content.decode('utf-8'), {})
        self.assertEqual(Check.objects.count(), 0)


class UncheckTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.the_user = User.objects.create_user(username='u', password='p')
        cls.task = Task.objects.create(
                name='testing', interval='10', created_by=cls.the_user)

    def setUp(self):
        self.client.force_login(self.the_user)

    def test_no_check_left(self):
        Check.objects.create(task=self.task, date='2016-01-15')
        self.assertEqual(Check.objects.count(), 1)

        response = self.client.post(reverse('uncheck'), {
            'task': self.task.pk,
            'date': '1/15/2016'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), {
            'last_date': None,
        })
        self.assertEqual(Check.objects.count(), 0)

    def test_get_past_check(self):
        Check.objects.create(task=self.task, date='2015-12-31')
        Check.objects.create(task=self.task, date='2016-01-15')
        self.assertEqual(Check.objects.count(), 2)

        response = self.client.post(reverse('uncheck'), {
            'task': self.task.pk,
            'date': '1/15/2016'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), {
            'last_date': '2015-12-31',
            'year': 2015,
            'month': 12,
            'day': 31,
        })
        self.assertEqual(Check.objects.count(), 1)

    def test_invalid_task(self):
        # Set invalid task value
        response = self.client.post(reverse('uncheck'), {
            'task': self.task.pk + 1,
            'date': '1/15/2016'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 400)
        self.assertTrue('task' in response.json())

    def test_other_user(self):
        self.client.force_login(
                User.objects.create_user(username='other_user', password='p'))

        Check.objects.create(task=self.task, date='2016-01-15')
        self.assertEqual(Check.objects.count(), 1)

        response = self.client.post(reverse('uncheck'), {
            'task': self.task.pk,
            'date': '1/15/2016'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Check is not deleted
        self.assertEqual(Check.objects.count(), 1)
        # TODO: It would be nice to response with error code and error message.
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), {
            'last_date': None
        })


class ArchivesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.the_user = User.objects.create_user(username='u', password='p')

        cls.task_checked = Task.objects.create(
                name='checked', interval='10', created_by=cls.the_user)
        cls.task_unchecked = Task.objects.create(
                name='unchecked', interval='10', created_by=cls.the_user)

        Check.objects.create(task=cls.task_unchecked, date='2016-01-15')
        Check.objects.create(task=cls.task_checked, date='2016-01-16')
        Check.objects.create(task=cls.task_unchecked, date='2016-01-17')

    def setUp(self):
        self.client.force_login(self.the_user)

    def test_no_check_left(self):
        response = self.client.get(reverse('archives', args=['2016', '01', '16']))

        self.assertEqual(response.status_code, 200)

        is_checked = response.context['is_task_checked']
        self.assertTrue(self.task_checked.pk in is_checked)
        self.assertTrue(self.task_unchecked.pk not in is_checked)

    def test_other_user(self):
        self.client.force_login(
                User.objects.create_user(username='other_user', password='p'))

        response = self.client.get(reverse('archives', args=['2016', '01', '16']))

        self.assertEqual(response.status_code, 200)

        # Other users must not see any of these
        self.assertFalse(response.context['tasks'])
        self.assertFalse(response.context['object_list'])
        self.assertFalse(response.context['is_task_checked'])


class CsvTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.the_user = User.objects.create_user(username='u', password='p')

        cls.task1 = Task.objects.create(
                name='1', interval='10', created_by=cls.the_user)
        cls.task2 = Task.objects.create(name='2', interval='10',
                created_by=cls.the_user)

        Check.objects.create(task=cls.task1, date='2016-01-15')
        Check.objects.create(task=cls.task1, date='2016-01-16')
        Check.objects.create(task=cls.task2, date='2016-01-16')
        Check.objects.create(task=cls.task2, date='2016-01-17')

    def setUp(self):
        self.client.force_login(self.the_user)

    def test_merge(self):
        response = self.client.get(reverse('csv'))

        self.assertContains(response, 'Date,1,2')
        self.assertContains(response, '2016-01-17,0,1')
        self.assertContains(response, '2016-01-16,1,1')
        self.assertContains(response, '2016-01-15,1,0')

    def test_other_user(self):
        self.client.force_login(
                User.objects.create_user(username='other_user', password='p'))

        response = self.client.get(reverse('csv'))

        self.assertEqual(response.content, b'Date\r\n')


class TrendsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.the_user = User.objects.create_user(username='u', password='p')

    def setUp(self):
        self.client.force_login(self.the_user)

    def test_bar_interval_7_days(self):
        task = Task.objects.create(
                name='t', interval='10', created_by=self.the_user)

        # Both beginning and the end of interval are checked (5/24-5/30)
        Check.objects.create(task=task, date='2015-05-30')
        Check.objects.create(task=task, date='2015-05-24')

        # An empty bar (5/17-5/23)

        # End of an interval is checked (5/10-5/16)
        Check.objects.create(task=task, date='2015-05-16')

        # An empty bar (5/3-5/9)

        # Beginning of an interval is checked (4/26 - 5/2)
        Check.objects.create(task=task, date='2015-04-26')

        response = self.client.post(reverse('trends_ajax'), {
            'date': '2015-05-30',
            'interval': '7',
        })

        self.assertJSONEqual(response.content.decode('utf-8'), {
            '10': [
                ['Date', 't'],
                ['4/12', 0],
                ['4/19', 0],
                ['4/26', 1],
                ['5/3', 0],
                ['5/10', 1],
                ['5/17', 0],
                ['5/24', 2]
            ],
            '20': None,
            'date': '2015-05-30',
            'interval': 7,
        })

    def test_bar_interval_30_days(self):
        task = Task.objects.create(
                name='t', interval='20', created_by=self.the_user)

        # Both beginning and the end of interval are checked (5/1-5/30)
        Check.objects.create(task=task, date='2015-05-01')
        Check.objects.create(task=task, date='2015-05-30')

        # An empty bar (4/1-4/30)

        # End of an interval is checked (3/2-3/31)
        Check.objects.create(task=task, date='2015-03-31')

        # An empty bar (1/31-3/1)

        # Beginning of an interval is checked (1/1 - 1/30)
        Check.objects.create(task=task, date='2015-1-1')

        response = self.client.post(reverse('trends_ajax'), {
            'date': '2015-05-30',
            'interval': '30',
        })

        self.assertJSONEqual(response.content.decode('utf-8'), {
            '10': None,
            '20': [
                ['Date', 't'],
                ['11/2', 0],
                ['12/2', 0],
                ['1/1', 1],
                ['1/31', 0],
                ['3/2', 1],
                ['4/1', 0],
                ['5/1', 2],
            ],
            'date': '2015-05-30',
            'interval': 30,
        })

    def test_other_user(self):
        self.client.force_login(
                User.objects.create_user(username='other_user', password='p'))

        task = Task.objects.create(
                name='t', interval='20', created_by=self.the_user)

        Check.objects.create(task=task, date='2015-05-01')

        response = self.client.post(reverse('trends_ajax'), {
            'date': '2015-05-30',
            'interval': '7',
        })

        # Other users must not see any task or check
        self.assertJSONEqual(response.content.decode('utf-8'), {
            '10': None,
            '20': None,
            'date': '2015-05-30',
            'interval': 7,
        })
