"""
URL configuration for sicgpt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include


from django.conf.urls import handler404, handler500, handler403, handler400
from core import views as core_views

handler404 = core_views.custom_page_not_found_view
handler500 = core_views.custom_error_view
handler403 = core_views.custom_permission_denied_view
handler400 = core_views.custom_bad_request_view


urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', include('registration.urls') ),
    path('', include('core.urls') ),
]
