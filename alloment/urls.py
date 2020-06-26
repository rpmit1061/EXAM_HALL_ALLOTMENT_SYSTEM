from django.urls import path,re_path
from . import views

urlpatterns = [
    path('data_sheet_upload/', views.data_sheet_upload, name="data_sheet_upload"),
    re_path(r'^delete/(?P<ids>[0-9]+)/$', views.delete_record, name='delete_record')
]