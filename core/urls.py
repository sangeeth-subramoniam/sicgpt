from django.urls import path,include
from . import views


from django.conf import settings
from django.conf.urls.static import static




app_name = 'core'

urlpatterns = [
    path('', views.home , name = "home"),
    path('<str:chatid>/', views.home , name = "home_with_parameters"),

    path('create_new_chat', views.create_new_chat , name = "create_new_chat"),
    
    
    path('change_session_name', views.change_session_name , name = "change_session_name"),
    
    
    
    path('errorpage/<str:error_text>', views.errorpage , name = "errorpage"),


    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)