from django.conf.urls import url

from checklist import views

urlpatterns = [
    url(r'^$', views.Main.as_view(), name='main'),
    url(r'^check/$', views.CheckCreate.as_view(), name='check'),
    url(r'^uncheck/$', views.CheckDelete.as_view(), name='uncheck'),
]
