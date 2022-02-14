from django.urls import path, re_path
from rest_framework.routers import SimpleRouter

from . import views
urlpatterns = [
    path('CalData/', views.Cal_sc.as_view(), name='portrait'),
    path('searchInfo/', views.SearchInfo.as_view(), name='portrait2'),
    path('downloads/', views.DownloadView.as_view(), name='downloads')
]
