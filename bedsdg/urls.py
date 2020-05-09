"""bedsdg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import i18n
from django.contrib.admin.sites import AdminSite
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.views.static import serve

from filebrowser.sites import site

from .views import home, index


site.storage._location = settings.MEDIA_ROOT
site.directory = "uploads/"

AdminSite.site_title = _('地球大数据SDG管理')
AdminSite.site_header = _('地球大数据SDG管理后台')


urlpatterns = [
    path('', index),
    path('home/', home, name='home'),
    path('article/', include('article.urls', namespace='article')),
    path('admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('i18n/', include(i18n)),
    path('tinymce/', include('tinymce.urls')),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
