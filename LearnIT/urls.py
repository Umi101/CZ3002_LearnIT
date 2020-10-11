from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from apps.questions.views.questions import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('admin/', admin.site.urls),

    path('', include('apps.accounts.urls')),
    path('questions/', include('apps.questions.urls')),
    path('markdownx/', include('markdownx.urls')),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__', include(debug_toolbar.urls)),)
