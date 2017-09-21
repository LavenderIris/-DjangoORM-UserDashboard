from django.conf.urls import url
from . import views           # This line is new!

urlpatterns = [
    url(r'^$', views.index),     # This line has changed!
    url(r'^add_user$', views.add_user), 
    url(r'^success$', views.success), 
    url(r'^login_process$', views.login), 
    url(r'^signin$', views.signin), 
    url(r'^register$', views.register), 
    url(r'^dashboard$', views.normaldashboard), 
    url(r'^dashboard/admin$', views.admindashboard), 
    url(r'^users/new$', views.admin_add_user), 
    url(r'^edit/user/(?P<id>[0-9]+)$', views.edit_user_admin), 
    url(r'^users/process_admin_edit$', views.process_admin_edit), 
]