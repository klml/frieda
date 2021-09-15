from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('internships', views.internships, name='internships'),
    re_path(r'organisations/?$', views.organisations, name='organisations'),

    re_path(r'organisation/?$', views.organisation, name='organisation'),
    re_path(r'organisation/(?P<pk>\d+)/$', views.organisation, name='organisation'),

    path('internship_organisation.csv', views.internship_organisation_csv, name='internship_organisation_csv'),
    
    path('contact', views.content, name='content'),
]
