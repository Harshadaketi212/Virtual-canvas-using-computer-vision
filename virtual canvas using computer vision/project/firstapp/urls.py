from django.urls import path 
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('detection',views.detection,name='detection'),
    path('download_pdf',views.download_pdf,name='download_pdf'),
    path('download_python_file',views.download_python_file,name='download_python_file'),
    path('login',views.logins,name='login'),
    path('logout',views.logouts,name='logout'),

]
