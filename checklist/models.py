from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):
    DAY = '10'
    WEEK = '20'
    INTERVAL_CHOICES = (
        (DAY, 'Daily'),
        (WEEK, 'Weekly'),
    )

    name = models.CharField(max_length=128)
    interval = models.CharField(max_length=2,
            choices=INTERVAL_CHOICES, default=DAY)
    datetime_update = models.DateTimeField(auto_now=True)
    datetime_create = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)

    def __unicode__(self):
        return ' - '.join([
            self.name,
            dict(Task.INTERVAL_CHOICES)[self.interval]
        ])

    class Meta:
        ordering = ['interval', 'name']


class Check(models.Model):
    task = models.ForeignKey(Task)
    date = models.DateField()
    datetime_create = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return ' | '.join([
                unicode(self.task),
                self.date.isoformat(),
                ''.join([
                    '(',
                    self.datetime_create.replace(microsecond=0).isoformat(b' '),
                    ')'
                ])
            ])

    class Meta:
        ordering = ['-date']
