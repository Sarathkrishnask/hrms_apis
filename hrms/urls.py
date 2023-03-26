"""hrms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from drf_yasg2 import openapi
from drf_yasg2.views import get_schema_view
from rest_framework import permissions
from utils import json
from django.contrib import admin


def render_react(request):
    return json.Response({"data":[]},"URL NOT FOUND",404,False)
# Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="HRMS",
        default_version='v1',
        description="HRMS API created using Django Rest Framework",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('api-docs', RedirectView.as_view(pattern_name='schema-swagger-ui')),
    path('api-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/user/', include('apps.user.urls')),
    path('api/admin/', include('apps.admin.urls')),
    path('api/account/',include('apps.account.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        re_path(r"^$", render_react),
        re_path(r"^(?:.*)/?$", render_react)
    ]

