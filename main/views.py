import json
import random
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import logging
from django.db.models import Q
from datetime import datetime, timedelta, date
from main.models import Client, DictPunkt, InfoDt, LastDt
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.db.models import DateField
from django.db.models.functions import Cast
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
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
        return HttpResponseRedirect('/set_delivery')


def set_delivery(request):
    if request.method != "POST":
        return render(request,  "select_delivery.html", {'login': f'{request.user.username}'})
    data = request.POST

    stat = -1
    # stat - с каких пвз выдаем товары
    # если stat = 1 - то выдаем с парнерских
    # если stat = 2 - то выдаем с непартнерских
    # если stat = 3 - то выдаем со всех пвз
    # если стат = 0, то просим заново пользователя отправить данные и нажать на чекбоксы

    if 'send to partner pvz' in data and 'send to NOpartner pvz' in data:
        stat = 3
    elif 'send to NOpartner pvz' in data:
        stat = 2
    elif 'send to partner pvz' in data:
        stat = 1
    else:
        stat = 0
    # print(stat)
    if not stat:
         return render(request, "select_delivery_error.html", {'login': f'{request.user.username}'})

    now = timezone.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    # Query to retrieve rows where date_action is within the current day and action is 1
    results = InfoDt.objects.filter(date_action__range=(start_of_day, end_of_day), action=1)
    # print(type(results))
    if results:
        return render(request, "Set_data_was.html", {'login': f'{request.user.username}'})
    Client_pvz = [] # у нас всё хранится типа: [[client_id, pvz]]

    list_mp = ['WB', 'wb', 'WB', 'wB']
    yesterday = timezone.now() - timedelta(days=2)
    start_of_yesterday = datetime(yesterday.year, yesterday.month, yesterday.day)
    end_of_yesterday = start_of_yesterday + timedelta(days=100)

    def buy_cl_pvz(client, pvz):
        if [client, pvz] in Client_pvz:
            # print('Clientid and PVZ is in list, because i dont work with it)')
            return
        PVZ_clients = Client.objects.filter(
        punkt_vidachi=pvz,
        clientid=client,
        status=3,
        punkt_vidachi__isnull=False,
        date_get__isnull=True,
        status_pizdec__isnull=True,
        date_active__gte=start_of_yesterday,
        date_active__lt=end_of_yesterday
        ).all()
        counter = 0
        for m in PVZ_clients:
            last = LastDt.objects.filter(client_id=m.id).exclude(action=2).first()
            if last != None:
                # print(f'Last of clientid:{m.id} exists, SKIP')
                continue
            counter += 1
            new_info = InfoDt(
                client_id=m.id,
                action=1,
                date_action=timezone.now(),
                person=user.id,
                clientid=m.clientid,
                phone=m.phone,
                barcode=m.barcode,
                pvz=pvz,
                code=m.code,
                code_qr=m.code_qr,
                price=m.price,
                task1=m.task1,
                date_active=m.date_active,
                naming=m.naming,
                article=m.article
            )
            new_info.save()
            Last = LastDt.objects.filter(client_id=m.id).first()
            # print(Last)
            if Last == None:
                last_info = LastDt(
                    client_id=m.id,
                    action=1,
                    date_last_action=timezone.now(),
                    person=user.id,
                    clientid=m.clientid,
                    phone=m.phone,
                    barcode=m.barcode,
                    pvz=pvz,
                    code=m.code,
                    code_qr=m.code_qr,
                    price=m.price,
                    task1=m.task1,
                    date_active=m.date_active,
                    naming=m.naming,
                    article=m.article
                )
                last_info.save()
            else:
                Last.date_last_action = timezone.now()
                Last.action = 1
                Last.save()



        Client_pvz.append([client, pvz])
        print(f'succesfully made adding to delivery all data with pvz:{pvz}, clientid:{client}, amount={counter}')
        return


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
    partner_pvz = DictPunkt.objects.filter(partner_status=1).values_list('id', flat=True)
    # print(partner_pvz)
    ll = LastDt.objects.filter(action=2).all()
    for Last in ll:
        buy_cl_pvz(Last.clientid, Last.pvz)



    for m in clients:
        z = random.randint(0, 100)
        try:
            ppvz = int(m.punkt_vidachi)
        except:
            ppvz = 0
        if stat == 1:
            if ppvz in partner_pvz:
                pass
            else:
                # print(f'SKIP, because pvz {ppvz} is not in partner pvz {partner_pvz}')
                continue
        elif stat == 2:
            if ppvz in partner_pvz:
                continue
        clientid = m.clientid
        if z <= 20:
            buy_cl_pvz(clientid, ppvz)

    # print(InfoDt.objects.all())
    today = timezone.now().strftime('%Y%m%d')
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
    today = timezone.now()
    start_of_today = datetime(today.year, today.month, today.day)
    print(formatted_date)
    for_deliver = InfoDt.objects.filter(date_action__date=formatted_date, action=1)
    print(for_deliver)
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
            "date_active": i.date_active.strftime('%Y.%m.%d'),
            "naming": i.naming, #naming
            "task1": i.task1,
            "who_give": i.who_gave
        }
        data['table'].append(table_object)

    l = json.dumps(data)
    # print(l)
    return render(request, "delivery_detail.html", data)
    # return HttpResponse(f"page for date: {formatted_date}")

def delivery_history(request):
    if request.method == "POST":
        pass
    infoDT = InfoDt.objects.all()

    daily_counts = InfoDt.objects.annotate(
        date=TruncDate('date_action')
    ).values('date').annotate(
        count_action1=Count('id', filter=Q(action=1)),
        count_action2=Count('id', filter=Q(action=2))
    ).order_by('date')

    # Loop through the results


    data = {
        'login': f'{request.user.username}',
        'rows': []
    }

    for entry in daily_counts:
        date = entry['date'].strftime('%d.%m.%Y')
        n1 = entry['count_action1']
        n2 = entry['count_action2']
        dat = {
            "date": date,
            "couriers": "В разработке",
            "get": f"{n2} из {n1}",
            "status": random.randint(0, 1),
            "redirect_url": f"delivery/{entry['date'].strftime('%Y%m%d')}/"
        }
        data["rows"].append(dat)
    print(data)

    return render(request, "History.html", data)


def couriers_history(request):
    if request.method == "POST":
        pass
    infoDT = InfoDt.objects.all()

    daily_counts = InfoDt.objects.annotate(
        date=TruncDate('date_action')
    ).values('date').annotate(
        count_action1=Count('id', filter=Q(action=1)),
        count_action2=Count('id', filter=Q(action=2))
    ).order_by('date')

    # Loop through the results


    data = {
        'login': f'{request.user.username}',
        'rows': []
    }

    for entry in daily_counts:
        date = entry['date'].strftime('%d.%m.%Y')
        n1 = entry['count_action1']
        n2 = entry['count_action2']
        dat = {
            "date": date,
            "couriers": "В разработке",
            "get": f"{n2} из {n1}",
            "status": random.randint(0, 1),
            "redirect_url": f"couriers/{entry['date'].strftime('%Y%m%d')}/"
        }
        data["rows"].append(dat)
    print(data)

    return render(request, "History.html", data)




def trry(request):

    distinct_dates = InfoDt.objects.annotate(date=Cast('date_action', output_field=DateField())).values_list('date', flat=True).distinct()
    distinct_dates_list = list(distinct_dates)

    daily_counts = InfoDt.objects.annotate(
        date=TruncDate('date_action')
    ).values('date').annotate(
        count_action1=Count('id', filter=Q(action=1)),
        count_action2=Count('id', filter=Q(action=2))
    ).order_by('date')

    # Loop through the results
    for entry in daily_counts:
        date = entry['date']
        count_action1 = entry['count_action1']
        count_action2 = entry['count_action2']
        print(f"Date: {date}, Action 1 Count: {count_action1}, Action 2 Count: {count_action2}")

    # print(distinct_dates_list)
    return HttpResponse("ALL DONE")
