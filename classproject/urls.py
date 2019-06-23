"""classproject URL Configuration

The `urlpatterns` list routes URLs to viewss. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function viewss
    1. Add an import:  from my_app import viewss
    2. Add a URL to urlpatterns:  path('', viewss.home, name='home')
Class-based viewss
    1. Add an import:  from other_app.viewss import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from onlineapp import viewss

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('hello/',viewss.hello_world),
    #path('get_clg_name/',viewss.get_my_college),
    #path('get_all_clgs/',viewss.get_all_colleges),
    #path('get_all_clgst/',viewss.get_all_colleges_temp),
]

from django.conf import settings
from django.urls import include, path  # For django versions from 2.0 and up

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
        path(r'',include('onlineapp.urls'))

    ] + urlpatterns