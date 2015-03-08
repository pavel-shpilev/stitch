from django.conf.urls import url, include
from django.contrib import admin

from taskboard.views import BoardList, BoardView, LabelView, MemberList, MemberView


urlpatterns = [
    url(r'^boards/$', BoardList.as_view()),
    url(r'^board/(?P<pk>[0-9]+)/$', BoardView.as_view()),
    url(r'^label/(?P<pk>[0-9]+)/$', LabelView.as_view()),
    url(r'^members/$', MemberList.as_view()),
    url(r'^member/(?P<pk>[0-9]+)/$', MemberView.as_view()),

    url(r'^admin/', include(admin.site.urls)),
]
