from django.db.models import Max
from django.shortcuts import render
from django.views import generic

from .models import Task

class Main(generic.ListView):
    template_name = "checklist/main.html"

    def get_queryset(self):
        return (Task.objects
                .annotate(last_date=Max('check__date'))
                .order_by('interval', 'last_date'))
