from django.conf.urls import url, include
from django.contrib import admin

from taskboard.views import BoardList, BoardView


urlpatterns = [
    url(r'^$', BoardList.as_view()),
    url(r'^board/(?P<pk>[0-9]+)/$', BoardView.as_view()),

    url(r'^admin/', include(admin.site.urls)),
]
