from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login


def auth(request):
    if request.method != "POST":
        if request.user.is_authenticated:
            return HttpResponse("Вы уже авторизованы!")
        return render(request, "Auth_page.html")

    User = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
    if User is None:
        return render(request, "Auth_page_err.html")
    return HttpResponseRedirect('/')
