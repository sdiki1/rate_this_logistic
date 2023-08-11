from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login

# Create your views here.
def auth(request):
    if request.method != "POST":
        if request.user.is_authenticated:
            return HttpResponse("Вы уже авторизованы!")
        return render(request, "mobile_auth.html")

    User = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
    if User is None:
        return render(request, "mobile_auth.html")
    login(request, User)
    return HttpResponseRedirect('/')


def main(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('auth')
    # print(request.user)
    return HttpResponse("lol")
