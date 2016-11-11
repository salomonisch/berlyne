from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='wui_index'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^accounts/', include(
        [
            url(r'^profile/$', views.profile, name='wui_acc_profile'),
            url(r'^', include('django.contrib.auth.urls')),
        ]
    )),
    url(r'^course_create$', views.course_edit, name='wui_course_create'),
    url(r'^course/$', views.courses, name='wui_courses'),
    url(r'^course/(?P<course_slug>[\w-]+)/', include(
        [
            url(r'^edit/$', views.course_edit, name='wui_course_edit'),
            url(r'^$', views.course_show, name='wui_course_show'),
            url(r'^delete/$', views.course_delete, name='wui_course_delete'),
            url(r'^join/$', views.course_join, name='wui_course_join'),
            url(r'^join_pw/$', views.course_join_pw, name='wui_course_join_pw'),
            url(r'^leave/$', views.course_leave, name='wui_course_leave'),
            url(r'^problems/$', views.course_problems, name='wui_course_problems'),
            url(r'^scoreboard/$', views.course_scoreboard, name='wui_course_scoreboard'),
            url(r'^manage_problems/$', views.course_manage_problems, name='wui_course_manage_problems'),
            url(r'^manage_points/$', views.course_manage_points, name='wui_points_to_problems')
        ]
    )),
]