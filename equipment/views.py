from django.shortcuts import render
from django.views.generic import ListView
from equipment.models import Equipment

class EquipmentList(ListView):
    model = Equipment


# Create your views here.
