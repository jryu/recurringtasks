from django.conf.urls import url

from checklist import views

urlpatterns = [
    url(r'^$', views.Main.as_view(), name='main'),
    url(r'^check/$', views.CheckCreate.as_view(), name='check'),
    url(r'^uncheck/$', views.CheckDelete.as_view(), name='uncheck'),

    url(r'^tasks/$', views.TaskList.as_view(), name='task_list'),
    url(r'^tasks/create/$', views.TaskCreate.as_view(), name='task_create'),
    url(r'^tasks/update/(?P<pk>\d+)$',
        views.TaskUpdate.as_view(), name='task_update'),
    url(r'^tasks/delete/(?P<pk>\d+)$',
        views.TaskDelete.as_view(), name='task_delete'),

    url(r'^archives/(?P<year>[0-9]{4})-(?P<month>[0-9]+)-(?P<day>[0-9]+)/$',
        views.Archives.as_view(month_format='%m'), name='archives'),

    url(r'^csv/$', views.DownloadCsv.as_view(), name='csv'),
]
