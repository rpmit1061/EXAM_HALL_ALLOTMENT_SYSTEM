from django.urls import path, re_path
from . import views

urlpatterns = [
    path('data_sheet_upload/', views.data_sheet_upload, name="data_sheet_upload"),
    re_path(r'^delete/(?P<ids>[0-9]+)/$', views.delete_record, name='delete_record'),
    re_path(r'^delete_room/(?P<idss>[0-9]+)/$', views.delete_room, name="delete_room"),
    path('room_maintenance/', views.room_maintenance, name='room_maintenance'),
    path('allotment/', views.allotment, name='allotment'),
    path('allotment2', views.allotment2, name='allotment2'),
    path('allotment3', views.allotment3, name='allotment3'),
    path("report", views.report, name='report')
]