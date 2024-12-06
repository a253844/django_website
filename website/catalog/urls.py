from django.urls import path
from . import tests
from . import views

urlpatterns = [
    path('test/', tests.testdb),
    path('admin/', tests.getadmin),
    path('Doctors/', views.getDoctors),
    path('Records/', views.getMedicalRecords),
    path('Patients/', views.getPatients),
    path('Schedules/', views.getSchedules),
    path('Costs/', views.getTreatmentCosts),
]