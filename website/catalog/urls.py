from django.urls import path
from . import tests, views
from django.contrib import admin

urlpatterns = [
    #admin
    #path('admin/', admin.site.urls),

    # tests
    path('test/', tests.testdb),
    path('getadmin/', tests.getadmin),
    path('createadmin/', tests.createadmin),
    path('updateadmin/', tests.updateadmin),
    path('updateadminPassword/', tests.updateadminPassword),
    path('deleteadmin/', tests.deleteadmin),

    # views
    path('Doctors/', views.getDoctors),
    path('Records/', views.getMedicalRecords),
    path('Patients/', views.getPatients),
    path('Schedules/', views.getSchedules),
    path('Costs/', views.getTreatmentCosts),
]