import os
import random
import string

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login

from PROMORTION import settings
from main.models import Client, DictPunkt, InfoDt, LastDt, Courier, Couriers_shifts, Users, problems
from datetime import datetime
from django.utils import timezone

# Create your views here.
def auth(request):
    if request.method != "POST":
        # if request.user.is_authenticated:
            # return HttpResponse("Вы уже авторизованы!")
        return render(request, "mobile_auth.html")

    User = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
    if User is None:
        print("INCORRECT LOGIN/PASSWORD")
        return render(request, "mobile_auth.html")

    login(request, User)
    return HttpResponseRedirect('/carrier/')

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

        photo_lin = f'https://{bask}.wb.ru/vol{l}/part{m}/{article}/images/big/1.jpg'
        return photo_lin


def main(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('auth')
    # print(request.user)
    user = request.user
    shift = user.id_shift
    print(shift)
    products = LastDt.objects.filter(action__in=[1,6,7,8], who_gave=int(shift))

    adresses = []
    for i in products:
        if i.pvz in adresses:
            continue
        adresses.append(i.pvz)
    # print(adresses)
    # print(products)
    data = {
        'login': f'{request.user.username}',
        'products': []
    }
    today = datetime.now()
    for i in adresses:
        products = LastDt.objects.filter(action__in=[1,6,7,8],  who_gave=int(shift), pvz=i) #date_last_action__date=today.date(),
        tmp = {
            'adress': DictPunkt.objects.filter(id=i).values_list('punkt_vidachi', flat=True).first(),
            "prods": []
        }
        for i in products:
            status = 0
            if i.action == 6:
                status = 0
            elif i.action == 7:
                status = 1
            elif i.action == 8:
                status = 2
            client = Client.objects.filter(id=i.client_id).first()
            tmp_2 = {
                "status": status,
                "name": client.name,
                "photo": photo_link(int(i.article)),
                "phone": i.phone,
                "code": i.code,
                "redirect_data": i.client_id
            }
            tmp["prods"].append(tmp_2)
        data["products"].append(tmp)
    print(data)
    return render(request, "mobile_main.html", data)


def product(request, data):
    if request.method == 'POST':
        user = request.user
        print(request.POST)
        if "Get_product" in request.POST:
            print('add all data')
            last = LastDt.objects.filter(client_id=int(data)).first()
            new_info = InfoDt(
                client_id=last.client_id,
                action=7,
                date_action=timezone.now(),
                person=user.id,
                clientid=last.clientid,
                phone=last.phone,
                barcode=last.barcode,
                pvz=last.pvz,
                code=last.code,
                code_qr=last.code_qr,
                price=last.price,
                task1=last.task1,
                date_active=last.date_active,
                naming=last.naming,
                article=last.article
            )
            new_info.save()
            last.action = 7
            last.date_last_action = timezone.now()
            last.save()
            return HttpResponseRedirect('/carrier')
        if "Dont_get" in request.POST:
            return HttpResponseRedirect(f'/carrier/product/{data}/problem1')
        if "Dont_know" in request.POST:
            return HttpResponseRedirect(f'/carrier/product/{data}/problem2')
        if "Check_problem" in request.POST:
            last = LastDt.objects.filter(client_id=int(data)).first()
            print(last)
            client = Client.objects.filter(id=int(data)).first()

            problem = problems.objects.filter(client_id=int(data)).first()

            if problem is None or problem.status_solving == 1:  # 1 статус решения 1 это когда выдали также товар,мы даём доступ человеку получить товар
                stat = 1
            elif problem.status_solving is None or problem.status_solving == 0:
                stat = 4
            elif problem.status_solving > 0:
                stat = 2
            else:
                stat = 1
            data = {
                'login': f'{request.user.username}',
                'product': {
                    "name": client.name,
                    "img": photo_link(int(last.article)),
                    "phone": last.phone,
                    "naming": client.naming,
                    "status_vidacha": True,
                    "mp": client.mp,
                    "barcode": last.barcode,
                    "code": last.code,
                    "code_qr": last.code_qr,
                },
                "status": stat,
            }
            # print(data)
            return render(request, "mobile_product.html", data)

    # return HttpResponse(f'{data}')
    last = LastDt.objects.filter(client_id=int(data)).first()
    print(last)
    client = Client.objects.filter(id=int(data)).first()

    problem = problems.objects.filter(client_id=int(data)).first()

    if problem is None or problem.status_solving == 1: #1 статус решения 1 это когда выдали также товар,мы даём доступ человеку получить товар
        stat = 1
    elif problem.status_solving is None or problem.status_solving == 0:
        stat = 3
    elif problem.status_solving > 0:
        stat = 2
    else:
        stat = 1
    # stat = 4
    data = {
        'login': f'{request.user.username}',
        'product': {
            "name": client.name,
            "img": photo_link(int(last.article)),
            "phone": last.phone,
            "naming": client.naming,
            "status_vidacha": True,
            "mp": client.mp,
            "barcode": last.barcode,
            "code": last.code,
            "code_qr": last.code_qr,
        },
        "status": stat,
    }
    # print(data)
    return render(request, "mobile_product.html", data)


def problem1(request, dat):
    if request.method == "POST":
        data = request.POST
        print(request.FILES)
        def generate_random_string(length):
            characters = string.ascii_letters + string.digits
            random_string = ''.join(random.choice(characters) for _ in range(length))
            return random_string + ".png"
        # import shutil
        folder_path = os.path.join(settings.MEDIA_ROOT, 'problem_photos')
        # if os.path.exists(folder_path):
        #     shutil.rmtree(folder_path)


        # Создаем папку, если ее нет
        os.makedirs(folder_path, exist_ok=True)

        # Обработка загруженных файлов
        names = []
        for uploaded_file in request.FILES.getlist("photo1"):
            name = generate_random_string(20)
            print(name)
            names.append(name)
            file_path = os.path.join(folder_path, name)
            print(file_path)
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        new_problem = problems(
            shift_id=request.user.id_shift,
            client_id=int(dat),
            status_problem=3,
            descriprion_problem=data['reason'],
            barcode_problem=data['barcode'],
            article_problem=data['article'],
            date_problem=timezone.now(),
            photo=" ".join(names)
        )
        new_problem.save()



        return HttpResponse(str(names))

    # print(request.method)

    if request.method == "POST":
        print(dat)
    client = Client.objects.filter(id=int(dat)).first()

    data = {
        "name": client.name,
        "id": dat,
    }
    return render(request, "mobile_problems.html", data)


def problem2(request, dat):
    if request.method == "POST":
        data = request.POST
        print(request.FILES)

        def generate_random_string(length):
            characters = string.ascii_letters + string.digits
            random_string = ''.join(random.choice(characters) for _ in range(length))
            return random_string + ".png"

        # import shutil
        folder_path = os.path.join(settings.MEDIA_ROOT, 'problem_photos')
        # if os.path.exists(folder_path):
        #     shutil.rmtree(folder_path)

        # Создаем папку, если ее нет
        os.makedirs(folder_path, exist_ok=True)

        # Обработка загруженных файлов
        names = []
        for uploaded_file in request.FILES.getlist("photo1"):
            name = generate_random_string(20)
            print(name)
            names.append(name)
            file_path = os.path.join(folder_path, name)
            print(file_path)
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        new_problem = problems(
            shift_id=request.user.id_shift,
            client_id=int(dat),
            status_problem=2,
            descriprion_problem=data['reason'],
            barcode_problem=data['barcode'],
            article_problem=data['article'],
            date_problem=timezone.now(),
            photo=" ".join(names)
        )
        new_problem.save()

        # return HttpResponse(str(names))

    # print(request.method)

    # if request.method == "POST":
    #     print(dat)
    client = Client.objects.filter(id=int(dat)).first()

    data = {
        "name": client.name,
        "id": dat,
    }
    return render(request, "mobile_problems.html", data)
