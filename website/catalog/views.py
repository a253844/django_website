from django.shortcuts import render
from catalog.models import Doctors, MedicalRecords, Patients, TreatmentCosts, Schedules
from django.http import HttpResponse 

# Create your views here.

def getDoctors(request):
    response = ""
    doctors = Doctors.objects.all()
    for var in doctors:
        response += var.first_name + " " + var.last_name + "醫師"

    return HttpResponse("<p>" + response + "</p>")


def getMedicalRecords(request):
    response = ""
    records = MedicalRecords.objects.all()
    for var in records:
        response += var.patient.first_name + "病患由 " + var.doctor.first_name + "醫師治療"

    return HttpResponse("<p>" + response + "</p>")

def getPatients(request):
    response = ""
    patients = Patients.objects.all()
    for var in patients:
        response += var.first_name + " " + var.last_name + "病患"

    return HttpResponse("<p>" + response + "</p>")

def getSchedules(request):
    response = ""
    schedules = Schedules.objects.all()
    for var in schedules:
        response += var.doctor.first_name + " " + var.doctor.last_name + "醫師值班時間為" + var.schedule_date 

    return HttpResponse("<p>" + response + "</p>")

def getTreatmentCosts(request):
    response = ""
    Costs = TreatmentCosts.objects.all()
    for var in Costs:
        response += var.medical_record.patient.first_name + " " + var.medical_record.patient.last_name + "病患於" + str(var.medical_record.visit_date) + "日治療，收取" + str(var.cost) + "元"

    return HttpResponse("<p>" + response + "</p>")
