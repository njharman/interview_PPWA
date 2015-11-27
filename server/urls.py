from django.conf.urls import include, url
from django.contrib import admin

import ppwa.urls


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^purchase/', include(ppwa.urls)),
    ]
