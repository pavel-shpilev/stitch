from django.conf.urls import url, include
from django.contrib import admin

from taskboard.views import BoardList, BoardView, LabelView, MemberList, MemberView, \
    ColumnList, ColumnView


urlpatterns = [
    url(r'^boards/(?P<board_id>[0-9]+)/columns/$', ColumnList.as_view()),  # List + create columns.
    url(r'^boards/(?P<pk>[0-9]+)/$', BoardView.as_view()),  # Rename + archive board.
    url(r'^boards/$', BoardList.as_view()),  # List + create boards.
    url(r'^columns/(?P<pk>[0-9]+)/$', ColumnView.as_view()),  # Rename + archive + reorder.
    url(r'^labels/(?P<pk>[0-9]+)/$', LabelView.as_view()),  # Rename label.
    url(r'^members/(?P<pk>[0-9]+)/$', MemberView.as_view()),  # Rename member.
    url(r'^members/$', MemberList.as_view()),  # List + create members.


    url(r'^admin/', include(admin.site.urls)),
]
