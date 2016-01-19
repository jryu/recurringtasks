from django.core.urlresolvers import reverse
from django.test import TestCase

from models import Check, Task

class CheckTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.task = Task.objects.create(name='testing', interval='10')

    def test_date_in_response(self):
        response = self.client.post(reverse('check'), {
            'task': self.task.pk,
            'date': '1/15/2016'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'pk': self.task.pk,
            'year': 2016,
            'month': 1,
            'day': 15
        })

    def test_invalid_task(self):
        # Set invalid task value
        response = self.client.post(reverse('check'), {
            'task': self.task.pk + 1,
            'date': '1/15/2016'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 400)
        self.assertTrue('task' in response.json())


class UncheckTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.task = Task.objects.create(name='testing', interval='10')

    def test_no_check_left(self):
        Check.objects.create(task=self.task, date='2016-01-15')

        response = self.client.post(reverse('uncheck'), {
            'task': self.task.pk,
            'date': '1/15/2016'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'last_date': None,
        })

    def test_get_past_check(self):
        Check.objects.create(task=self.task, date='2015-12-31')
        Check.objects.create(task=self.task, date='2016-01-15')

        response = self.client.post(reverse('uncheck'), {
            'task': self.task.pk,
            'date': '1/15/2016'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'last_date': '2015-12-31',
            'year': 2015,
            'month': 12,
            'day': 31,
        })

    def test_invalid_task(self):
        # Set invalid task value
        response = self.client.post(reverse('uncheck'), {
            'task': self.task.pk + 1,
            'date': '1/15/2016'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 400)
        self.assertTrue('task' in response.json())


class ArchivesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.task_checked = Task.objects.create(name='checked', interval='10')
        cls.task_unchecked = Task.objects.create(name='unchecked', interval='10')

        Check.objects.create(task=cls.task_unchecked, date='2016-01-15')
        Check.objects.create(task=cls.task_checked, date='2016-01-16')
        Check.objects.create(task=cls.task_unchecked, date='2016-01-17')

    def test_no_check_left(self):
        response = self.client.get(reverse('archives', args=['2016', '01', '16']))

        self.assertEqual(response.status_code, 200)

        is_checked = response.context['is_task_checked']
        self.assertTrue(self.task_checked.pk in is_checked)
        self.assertTrue(self.task_unchecked.pk not in is_checked)


class CsvTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.task1 = Task.objects.create(name='1', interval='10')
        cls.task2 = Task.objects.create(name='2', interval='10')

        Check.objects.create(task=cls.task1, date='2016-01-15')
        Check.objects.create(task=cls.task1, date='2016-01-16')
        Check.objects.create(task=cls.task2, date='2016-01-16')
        Check.objects.create(task=cls.task2, date='2016-01-17')

    def test_merge(self):
        response = self.client.get(reverse('csv'))

        self.assertContains(response, 'Date,1,2')
        self.assertContains(response, '2016-01-17,0,1')
        self.assertContains(response, '2016-01-16,1,1')
        self.assertContains(response, '2016-01-15,1,0')
