import random
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import logging
from django.db.models import Q
from datetime import datetime, timedelta, date
from main.models import Client, DictPunkt, InfoDt
from django.contrib.auth import authenticate, login
from django.utils import timezone

def main(request):
    if request.user.is_authenticated:
        return render(request, "main.html", {'login': f'{request.user.username}'})
    else:
        return HttpResponseRedirect('/auth/')


def delivery(request):
    if request.method != "POST":
        if request.user.is_authenticated:
            return render(request, "Delivery.html", {'login': f'{request.user.username}'})
        else:
            return HttpResponseRedirect('/auth/')
    if 'History' in request.POST:
        return HttpResponseRedirect("/delivery/history")
    elif 'setData' in request.POST:
        now = timezone.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        # Query to retrieve rows where date_action is within the current day and action is 1
        results = InfoDt.objects.filter(date_action__range=(start_of_day, end_of_day), action=1)
        print(type(results))
        if results:
            return render(request, "Set_data_was.html", {'login': f'{request.user.username}'})

        list_mp = ['WB', 'wb', 'WB', 'wB']
        yesterday = datetime.now() - timedelta(days=3)
        start_of_yesterday = datetime(yesterday.year, yesterday.month, yesterday.day)
        end_of_yesterday = start_of_yesterday + timedelta(days=10)

        user = request.user
        clients = Client.objects.filter(
            status=3,
            punkt_vidachi__isnull=False,
            date_get__isnull=True,
            status_pizdec__isnull=True,
            date_active__gte=start_of_yesterday,
            date_active__lt=end_of_yesterday,
        ).all()
        # adress = DictPunkt.objects.all()

        for m in clients:
            z = random.randint(0, 100)
            try:
                ppvz = int(m.punkt_vidachi)
            except:
                ppvz = 0
            if z <= 29:
                new_info = InfoDt(
                    client_id=m.id,
                    action=1,
                    date_action=datetime.now(),
                    person=user.id,
                    clientid=m.clientid,
                    phone=m.phone,
                    barcode=m.barcode,
                    pvz=ppvz,
                    code=m.code,
                    code_qr=m.code_qr,
                    price=m.price,
                    task1=m.task1,
                    date_active=m.date_active,
                    naming=m.naming,
                    article=m.article
                )
                new_info.save()
        # print(InfoDt.objects.all())
        today = datetime.now().strftime('%Y%m%d')
        return HttpResponseRedirect(f"/delivery/{today}/")

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


def delivery_detail(request, date):
    try:
        formatted_date = datetime.strptime(str(date), '%Y%m%d').date()
    except:
        print('ERROR')
        return HttpResponse("error")
    today = datetime.now()
    start_of_today = datetime(today.year, today.month, today.day)
    for_deliver = InfoDt.objects.filter(
        date_action__gte=start_of_today,
        action=1
    )

    status_dict = {
        1: "Корзина собирается",
        2: "Оплачен",
        3: "Получить",
        4: "Получен",
        5: "Опубликовать",
        6: "Модерация",
        7: "Опубликован",
        8: "Удалён",
        9: "Отмена",
        10: "Возврат",
        11: "Проверить",
        12: "Выдан курьеру",
        21: "Не нашел в выдаче"
    }
    data = {
        'login': f'{request.user.username}',
        'table': []
    }
    for i in for_deliver:
        # client = Client.objects.filter(id=i.client_id).first()
        table_object = {
            "id": i.client_id,
            # "status": status_dict[int(client.status)],
            "article": i.article,
            "barcode": i.barcode,
            "clientid": i.clientid,
            "name": i.name,
            "phone": i.phone,
            "punkt_vidachi": i.pvz,
            "code": i.code,
            "code_qr": i.code_qr,
            "date_active": i.date_active,
            "naming": i.naming, #naming
            "task1": i.task1,
            "who_give": i.who_gave
        }
        data['table'].append(table_object)
    # print(data)
    return render(request, "delivery_detail.html", data)
    # return HttpResponse(f"page for date: {formatted_date}")
