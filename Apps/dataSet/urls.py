from django.urls import path, re_path
from rest_framework.routers import SimpleRouter

from . import views
urlpatterns = [
    path('down/', views.DownloadView.as_view(), name='down'),
    path('adds/', views.Add_many.as_view(), name='adds')
]
#角色管理
router = SimpleRouter()
router.register(r"dataRules", views.DataRulesView, basename='dataRules')
urlpatterns += router.urls
