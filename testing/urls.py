from django.conf.urls import url
from testing import views

urlpatterns=[
url(r'^register/$', views.register, name='register'),
url(r'^first/$', views.first),
url(r'^login/$', views.user_login, name='login'),
url(r'^logout/$', views.user_logout, name='logout'),
url(r'^owncourse/$',views.list,name="list"),
url(r'^owncourse/(?P<pk>[0-9]+)/delete/$',views.coursedeleteview.as_view()),
url(r'^owncourse/(?P<pk>[0-9]+)/update/$',views.courseupdateview.as_view()),
url(r'^owncourse/(?P<pk>[0-9]+)/posts/$',views.postlist,name='posts'),
url(r'^owncourse/(?P<id>[0-9]+)/posts/(?P<pk>[0-9]+)/delete/$',views.postdeleteview.as_view()),
url(r'^owncourse/(?P<id>[0-9]+)/posts/(?P<pk>[0-9]+)/update/$',views.postupdateview.as_view()),
#url(r'^addcourse/$',views.coursecreateview.as_view()),
#url(r'^addposts/(?P<pk>[0-9]+)/$',views.postcreateview.as_view()),
    url(r'^join/$',views.allcourses,name="all"),
url(r'^enroll/(?P<pk>[0-9]+)/$',views.enroll),
url(r'^unenroll/(?P<pk>[0-9]+)/$',views.unenroll),
url(r'^posts/(?P<pk>[0-9]+)/$',views.postdetail),
        ]
