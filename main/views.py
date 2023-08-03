from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import logging
from django.contrib.auth import authenticate, login


def main(request):
    if request.user.is_authenticated:
        return render(request, "main.html", {'login': f'{request.user.username}'})
    else:
        return HttpResponseRedirect('/auth/')


def delivery(request):
    if request.user.is_authenticated:
        return render(request, "Delivery.html", {'login': f'{request.user.username}'})
    else:
        return HttpResponseRedirect('/auth/')


def courier(request):
    if request.user.is_authenticated:
        return render(request, "Courier.html", {'login': f'{request.user.username}'})
    else:
        return HttpResponseRedirect('/auth/')


def warehouse(request):
    if request.user.is_authenticated:
        return render(request, "Warehouse.html", {'login': f'{request.user.username}'})
    else:
        return HttpResponseRedirect('/auth/')
