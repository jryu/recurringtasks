import csv
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.db.models import Count, Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Check, Task
from .forms import CheckForm, TrendsForm

class Main(generic.ListView):
    template_name = "checklist/main.html"

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return super(Main, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return (Task.objects
                .annotate(last_date=Max('check__date'))
                .order_by('interval', 'last_date'))


# https://docs.djangoproject.com/en/1.9/topics/class-based-views/generic-editing/#ajax-example
class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            date = self.object.date
            data = {
                'pk': self.object.pk,
                'year': date.year,
                'month': date.month,
                'day': date.day,
            }
            return JsonResponse(data)
        else:
            return response


class CheckCreate(AjaxableResponseMixin, generic.edit.CreateView):
    model = Check
    fields = ['date', 'task']

    def get_success_url(self):
        return reverse('main')


class CheckDelete(generic.base.View):
    def post(self, request, *args, **kwargs):
        form = CheckForm(request.POST)
        if form.is_valid():
            Check.objects.filter(
                    task_id=form.cleaned_data['task'],
                    date=form.cleaned_data['date']).delete()

            last_date = (Check.objects
                    .filter(task_id=form.cleaned_data['task'])
                    .aggregate(Max('date'))['date__max'])

            response = {
              'last_date': last_date,
            }
            if last_date:
                response['year'] = last_date.year
                response['month'] = last_date.month
                response['day'] = last_date.day

            return JsonResponse(response)
        else:
            return JsonResponse(form.errors, status=400)


class TaskSuccessUrlMixin(object):
    def get_success_url(self):
        return reverse('task_list')


class TaskFieldsMixin(object):
    fields = ['name', 'interval']


class TaskList(generic.ListView):
    model = Task


class TaskDelete(TaskSuccessUrlMixin, generic.DeleteView):
    model = Task


class TaskUpdate(TaskSuccessUrlMixin, TaskFieldsMixin, generic.UpdateView):
    model = Task


class TaskCreate(TaskSuccessUrlMixin, TaskFieldsMixin,
        generic.edit.CreateView):
    model = Task


class Archives(generic.dates.DayArchiveView):
    model = Check
    date_field = 'date'
    allow_empty = True
    allow_future = True

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Archives, self).get_context_data(**kwargs)

        context['tasks'] = Task.objects.all()

        is_checked = {}
        for check in context['object_list']:
            is_checked[check.task.pk] = True
        context['is_task_checked'] = is_checked

        return context


class DownloadCsv(generic.base.View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="checklist.csv"'

        writer = csv.writer(response)

        row = ['Date']
        task_to_index = {}
        count = 1
        for task in Task.objects.all():
            row.append(task.name)
            task_to_index[task.pk] = count
            count += 1

        date_of_row = None
        for check in Check.objects.all():
            if check.date != date_of_row:
                writer.writerow(row)
                row = [0] * count
                row[0] = check.date
                date_of_row = check.date
            row[task_to_index[check.task.pk]] = 1
        writer.writerow(row)

        return response


class TrendsAjax(generic.base.View):
    def format_date(self, date):
        return date.strftime('%-m/%-d')

    def build_data(self, task_interval, date, count_interval):
        row = ['Date']
        task_to_index = {}
        for task in Task.objects.filter(interval=task_interval):
            task_to_index[task.pk] = len(row)
            row.append(task.name)

        # There is no task in this group
        if len(row) == 1:
            return None

        data = [row]

        last_day_of_interval = date
        last_day_of_next_interval = (last_day_of_interval -
                timedelta(days=count_interval))

        for _ in range(7):
            row = [0] * len(row)
            row[0] = self.format_date(
                    last_day_of_next_interval + timedelta(days=1))

            checks = (Check.objects
                .filter(
                    task__interval=task_interval,
                    date__lte=last_day_of_interval,
                    date__gt=last_day_of_next_interval)
                .values('task').order_by()
                .annotate(total=Count('task')))

            for check in checks:
                row[task_to_index[check['task']]] = check['total']
            data.insert(1, row)

            last_day_of_interval = last_day_of_next_interval
            last_day_of_next_interval = (last_day_of_interval -
                    timedelta(days=count_interval))

        return data


    def post(self, request, *args, **kwargs):
        form = TrendsForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            count_interval = form.cleaned_data['interval']

            return JsonResponse({
                Task.DAY: self.build_data(Task.DAY, date, count_interval),
                Task.WEEK: self.build_data(Task.WEEK, date, count_interval),
                'date': date,
                'interval': count_interval,
            })
        else:
            return JsonResponse(form.errors, status=400)
