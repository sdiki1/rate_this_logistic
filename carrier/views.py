from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from main.models import Client, DictPunkt, InfoDt, LastDt, Courier, Couriers_shifts, Users

# Create your views here.
def auth(request):
    if request.method != "POST":
        if request.user.is_authenticated:
            return HttpResponse("Вы уже авторизованы!")
        return render(request, "mobile_auth.html")

    User = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
    if User is None:
        print("INCORRECT LOGIN/PASSWORD")
        return render(request, "mobile_auth.html")

    login(request, User)
    return HttpResponseRedirect('')

def photo_link(article: int):
    l = article // (10 ** 5)
    m = article // (10 ** 3)
    # print(l, m)

    g = 0
    if l <= 143:
        g = 1
    elif l <= 287:
        g = 2
    elif l <= 431:
        g = 3
    elif l <= 719:
        g = 4
    elif l <= 1007:
        g = 5
    elif l <= 1061:
        g = 6
    elif l <= 1115:
        g = 7
    elif l <= 1169:
        g = 8
    elif l <= 1313:
        g = 9
    elif l <= 1601:
        g = 10
    elif l <= 1655:
        g = 11
    else:
        g = 12

    if g < 10:
        bask = f'basket-0{g}'
    else:
        bask = f'basket-{g}'

        photo_lin = f'https://{bask}.wb.ru/vol{l}/part{m}/{article}/images/tm/1.jpg'
        return photo_lin


def main(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('auth')
    # print(request.user)
    user = request.user
    shift = user.id_shift
    print(shift)
    products = LastDt.objects.filter(action=6, who_gave=int(shift))

    adresses = []
    for i in products:
        if i.pvz in adresses:
            continue
        adresses.append(i.pvz)
    print(adresses)
    # print(products)
    data = {
        'login': f'{request.user.username}',
        'products': []
    }

    for i in adresses:
        products = LastDt.objects.filter(action=6, who_gave=int(shift), pvz=i)

        tmp = {
            'adress': DictPunkt.objects.filter(id=i).values_list('punkt_vidachi', flat=True).first(),
            "prods": []
        }
        for i in products:
            tmp_2 = {
                "name": i.name,
                "photo": photo_link(int(i.article)),
                "phone": i.phone,
                "code": i.code,
                "redirect_data": i.client_id
            }
            tmp["prods"].append(tmp_2)
        data["products"].append(tmp)
    print(data)
    return render(request, "mobile_main.html", data)

