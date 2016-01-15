from django.conf.urls import url

from checklist import views

urlpatterns = [
    url(r'^$', views.Main.as_view(), name='main'),
]
