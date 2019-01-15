from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    url(r'^$', views.HomePageView, name='home'),
    path('ajax/load_court_types/', views.load_court_types, name='ajax_load_courts'),
    url(r'^about/$', views.AboutPageView.as_view(), name='about'),
    url(r'^contact/$', views.ContactPageView.as_view(), name='contact'),
    url(r'^scheduler/$', views.SchedulerPageView.as_view(), name='scheduler'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^signUpForTimes/$', views.signUpForTimes, name='signUpForTimes'),
]
