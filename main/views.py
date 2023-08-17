import random, openpyxl, json, string
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from datetime import datetime, timedelta
from main.models import Client, DictPunkt, InfoDt, LastDt, Courier, Couriers_shifts, Users, problems
from django.utils import timezone
from django.contrib.auth import logout
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
import pandas as pd
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
    yesterday = timezone.now() - timedelta(days=1)
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
            last = LastDt.objects.filter(client_id=m.id).exclude(action=3).first()
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
    ll = LastDt.objects.filter(action=3).all()
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
    if request.method != "POST":
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
        # if random.randint(0, 1):
        #     lol = True
        # else:
        #     lol = False

        last_obj = LastDt.objects.filter(action=1).first()
        print(formatted_date, datetime.today().date())
        print(last_obj)
        if last_obj is not None and formatted_date == datetime.today().date():
            is_active = True
        else:
            is_active = False

        data = {
            'login': f'{request.user.username}',
            'table': [],
            'is_active': is_active
        }
        for i in for_deliver:
            # client = Client.objects.filter(id=i.client_id).first()
            if i.pvz != 0:
                pvz_row = DictPunkt.objects.filter(id=i.pvz).first()
                pvz = pvz_row.punkt_vidachi
            else:
                pvz=0
            table_object = {
                "id": i.client_id,
                # "status": status_dict[int(client.status)],
                "article": i.article,
                "barcode": i.barcode,
                "clientid": i.clientid,
                "name": i.name,
                "phone": i.phone,
                "punkt_vidachi": pvz,
                "code": i.code,
                "code_qr": i.code_qr,
                "date_active": i.date_active.strftime('%Y.%m.%d'),
                "naming": i.naming, #naming
                "task1": i.task1,
                "who_give": i.who_gave,
                "price": i.price
            }
            data['table'].append(table_object)



        # l = json.dumps(data)
        # print(l)
        return render(request, "delivery_detail.html", data)
    else:
        if "excel" in request.POST:

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
            # if random.randint(0, 1):
            #     lol = True
            # else:
            #     lol = False

            last_obj = LastDt.objects.filter(action=1).first()
            print(formatted_date, datetime.today().date())
            print(last_obj)
            if last_obj is not None and formatted_date == datetime.today().date():
                is_active = True
            else:
                is_active = False

            data = []
            for i in for_deliver:
                # client = Client.objects.filter(id=i.client_id).first()
                if i.pvz != 0:
                    pvz_row = DictPunkt.objects.filter(id=i.pvz).first()
                    pvz = pvz_row.punkt_vidachi
                else:
                    pvz = 0
                table_object = {
                    "id": i.client_id,
                    # "status": status_dict[int(client.status)],
                    "article": i.article,
                    "barcode": i.barcode,
                    "clientid": i.clientid,
                    "name": i.name,
                    "phone": i.phone,
                    "punkt_vidachi": pvz,
                    "code": i.code,
                    "date_active": i.date_active.strftime('%Y.%m.%d'),
                    "naming": i.naming,  # naming
                    "task1": str(i.task1),
                    "who_give": i.who_gave,
                    "price": i.price
                }
                data.append(table_object)

            df = pd.DataFrame(data)

            excel_writer = pd.ExcelWriter('table_data.xlsx', engine='openpyxl')
            df.to_excel(excel_writer, sheet_name='Sheet1', index=False)

            # Настройка стиля для Excel файла (необязательно)
            workbook = excel_writer.book
            worksheet = excel_writer.sheets['Sheet1']
            for column_cells in worksheet.columns:
                length = max(len(str(cell.value)) for cell in column_cells)
                worksheet.column_dimensions[column_cells[0].column_letter].width = length

            excel_writer.close()  # Закрываем ExcelWriter

            # Создание HTTP Response с Excel файлом во вложении
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="table_data.xlsx"'
            with open('table_data.xlsx', 'rb') as excel_file:
                response.write(excel_file.read())

            return response
        if "dovidacha" in request.POST:
            print("return DOVIDACHA PAGE")
        if "end_delivery" in request.POST:
            user = request.user
            last_obj = LastDt.objects.filter(action=1).all()
            for i in last_obj:
                i.date_active = timezone.now()
                i.action = 2
                i.save()
                new_info = InfoDt(
                    client_id=i.client_id,
                    action=1,
                    date_action=timezone.now(),
                    person=user.id,
                    clientid=i.clientid,
                    phone=i.phone,
                    barcode=i.barcode,
                    pvz=i.pvz,
                    code=i.code,
                    code_qr=i.code_qr,
                    price=i.price,
                    task1=i.task1,
                    date_active=i.date_active,
                    naming=i.naming,
                    article=i.article
                )
                new_info.save()

        return HttpResponseRedirect(f"{request.path}")


def delivery_history(request):
    if request.method == "POST":
        pass

    daily_counts = InfoDt.objects.annotate(
        date=TruncDate('date_action')
    ).values('date').annotate(
        count_action1=Count('id', filter=Q(action=1)),
        count_action2=Count('id', filter=Q(action=3))
    ).order_by('date')
    # print(daily_counts)
    # Loop through the results


    data = {
        'login': f'{request.user.username}',
        'rows': []
    }

    for entry in daily_counts:
        date = entry['date'].strftime('%d.%m.%Y')
        n1 = entry['count_action1']
        n2 = entry['count_action2']
        last = LastDt.objects.filter(action=1).all()
        if last != [] and entry['date'] == timezone.datetime.today().date():
            status = 1
        else:
            status = 0
        dat = {
            "date": date,
            "couriers": "В разработке",
            "get": f"{n2} из {n1}",
            "status": status,
            "redirect_url": f"delivery/{entry['date'].strftime('%Y%m%d')}/"
        }
        data["rows"].append(dat)
    print(data)

    return render(request, "History.html", data)


def couriers_history(request):
    if request.method == "POST":
        pass
    infoDT = InfoDt.objects.all()


    # Loop through the results

    dates = Couriers_shifts.objects.annotate(date=TruncDate('start_shift')).values('date').distinct()
    print(dates)
    data = {
        'login': f'{request.user.username}',
        'rows': []
    }

    for entry in dates:
        entry = entry['date']
        shifts_on_specific_date = Couriers_shifts.objects.filter(Q(start_shift__date=entry))
        date = entry.strftime('%Y.%m.%d')
        counter = 0
        status = 0
        for m in shifts_on_specific_date:
            counter += 1
            if m.end_shift is None:
                status = 1
        dat = {
            "date": date,
            "couriers": counter,
            "status": status,
            "redirect_url": f"couriers/{entry.strftime('%Y%m%d')}/"
        }
        data["rows"].append(dat)
    print(data)

    return render(request, "History_courier.html", data)




def trry(request):

    return render(request, 'information.html', {'login': f'{request.user.username}'})


def send_couriers(request):
    if request.method == 'POST':
        print(request.POST)
        data = request.POST
        for m in range(len(data.getlist('name'))):
            if len(data.getlist('name')) < 2:
                break
            if data.getlist('name')[m] == '' or data.getlist("auto")[m] == '' or data.getlist("phone")[m] == '' or data.getlist("number")[m] == '' or data.getlist("where")[m] == '':
                couriers = Courier.objects.filter(is_partner_now=1).all()

                data = {
                    'login': f'{request.user.username}',
                    'couriers': []
                }
                for i in couriers:
                    courier = {
                        "id": f'{i.id}-idCourier',
                        "name": i.name,
                        "surname": i.surname,
                        "auto": i.auto_model,
                        "auto_number": i.auto_number,
                        "phone": i.phone
                    }
                    data['couriers'].append(courier)

                return render(request, 'send_courier_err.html', data)

        partner_pvz = 0

        if "send to NOpartner pvz" in data and "send to partner pvz" not in data:
            partner_pvz = 2
        if "send to NOpartner pvz" not in data and "send to partner pvz" in data:
            partner_pvz = 1

        for m in range(len(data.getlist('name'))):
            if data.getlist('name')[m] == '' or data.getlist("auto")[m] == '' or data.getlist("phone")[m] == '' or data.getlist("number")[m] == '' or data.getlist("where")[m] == '':
                continue
            name_courier = data.getlist('name')[m]
            auto_courier = data.getlist('auto')[m]
            auto_number = data.getlist('number')[m]
            phone_courier = data.getlist('phone')[m]
            where_courier = data.getlist('where')[m]
            new_shift = Couriers_shifts(
                name=name_courier,
                start_shift=timezone.now(),
                auto_number=auto_number,
                auto_model=auto_courier,
                phone=phone_courier,
                where_courier=where_courier,
                is_partner_pvz=partner_pvz
            )
            new_shift.save()

        couriers = Courier.objects.filter(is_partner_now=1).all()
        for i in couriers:
            if f'courier-{i.id}-idCourier' in data:
                new_shift = Couriers_shifts(
                    name=i.name,
                    start_shift=timezone.now(),
                    auto_number=i.auto_number,
                    auto_model=i.auto_model,
                    phone=i.phone,
                    where_courier="ШТАТ",
                    partner_id=i.id,
                    is_partner_pvz=partner_pvz
                )
                new_shift.save()

        return HttpResponseRedirect('/courier/send/pvz')

    couriers = Courier.objects.filter(is_partner_now=1).all()

    data = {
        'login': f'{request.user.username}',
        'couriers': []
    }
    for i in couriers:
        courier = {
            "id": f'{i.id}-idCourier',
            "name": i.name,
            "surname": i.surname,
            "auto": i.auto_model,
            "auto_number": i.auto_number,
            "phone": i.phone
        }
        data['couriers'].append(courier)
    print(data)
    return render(request, 'send_courier.html', data)




def set_pvz(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        couriers = Couriers_shifts.objects.filter(end_shift__isnull=True)
        adresses = []
        last = LastDt.objects.filter(action__in=[1, 4, 5, 8])
        partner = DictPunkt.objects.filter(partner_status=1).values_list('id', flat=True)
        print(partner)
        m = couriers[0].is_partner_pvz

        for i in last:
            if m == 1:
                if i.pvz not in partner:
                    continue
            if m == 2:
                if i.pvz in partner:
                    continue
            if i.pvz in adresses:
                continue
            adresses.append(i.pvz)
        courier_pvz = []

        for i in adresses:
            if data[f'{i}'] == '':
                continue
            block = {
                "pvz": str(i),
                "courier": data[f'{i}']
            }
            courier_pvz.append(block)
        l = m
        for i in courier_pvz:
            m = l
            pvz = i["pvz"]
            id = i["courier"]
            print('pvz:', pvz, "id:", id)
            if id == '' or id is None or id == 0:
                continue
            if m == 1:
                products = LastDt.objects.filter(action__in=[4, 5, 8]).filter(pvz=pvz)
            elif m == 2:
                products = LastDt.objects.filter(action__in=[1]).filter(pvz=pvz)
            else:
                products = LastDt.objects.filter(action__in=[1, 4, 5, 8]).filter(pvz=pvz)
            for m in products:
                if m.action in [4, 5, 8]:
                    m.action = 6
                else:
                    m.action = 1
                m.who_gave = id
                m.date_last_action = timezone.now()
                m.save()
                new_info = InfoDt(
                    client_id=m.client_id,
                    action=m.action,
                    date_action=timezone.now(),
                    person=m.id,
                    clientid=m.clientid,
                    phone=m.phone,
                    barcode=m.barcode,
                    pvz=m.pvz,
                    code=m.code,
                    code_qr=m.code_qr,
                    price=m.price,
                    task1=m.task1,
                    date_active=m.date_active,
                    naming=m.naming,
                    article=m.article,
                    who_gave=id,
                )
                m.save()
                new_info.save()

        def generate_random_string(length):
            characters = string.ascii_letters + string.digits
            random_string = ''.join(random.choice(characters) for _ in range(length))
            return random_string

        couriers = Couriers_shifts.objects.filter(end_shift__isnull=True)
        for i in couriers:
            pas = generate_random_string(6)
            i.login = f"courier_{i.id}"
            i.password = pas
            i.save()
            user = Users.objects.create_user(
                username=f"courier_{i.id}",
                password=pas,
                id_shift=f"{i.id}",
                phone=f"{i.phone}",
                status=2
            )
            user.save()

        return HttpResponseRedirect('/courier/send/set_data')


    data = {
        'login': f'{request.user.username}',
        'addresses': [],
        'couriers': [],
    }

    couriers = Couriers_shifts.objects.filter(end_shift__isnull=True)

    adresses = []
    last = LastDt.objects.filter(action__in=[1, 4, 5, 8])
    partner = DictPunkt.objects.filter(partner_status=1).values_list('id', flat=True)
    print(partner)
    m = couriers[0].is_partner_pvz
    print(m)
    print(last)

    for i in last:

        if m == 1:
            if i.pvz not in partner:
                continue
        if m == 2:
            if i.pvz in partner:
                continue
        if i.pvz in adresses:
            continue
        adresses.append(i.pvz)
    print(adresses)
    for i in couriers:
        data['couriers'].append({"name": i.name, "id": i.id})

    for i in adresses:
        adress_full = DictPunkt.objects.filter(id=i).values_list('punkt_vidachi', flat=True).first()
        data['addresses'].append({"id": i, "adress": adress_full})
    print(data)
    return render(request, 'set_pvz.html', data)


def set_data(request):
    if request.method == "POST":
        return HttpResponse("ЛОЛ, я хз чё делать если метод == пост, потом вова мб доработает эту хуйню")

    data = {
        'login': f'{request.user.username}',
        'couriers': [],
    }
    couriers = Couriers_shifts.objects.filter(end_shift__isnull=True)
    for i in couriers:
        tmp = {
            "id": i.id,
            "name": f"{i.name}",
            "auto": i.auto_model,
            "number": i.auto_number,
            "where": i.where_courier,
            "login": f"courier_{i.id}",
            "phone": i.phone,
            "password": i.password,
            "copy_data": f"ИМЯ: {i.name}, \nАВТО: {i.auto_number},\nНОМЕР АВТО: {i.auto_number}\n ТЕЛЕФОН: {i.phone} \n\nЛОГИН: courier_{i.id}\n ПАРОЛЬ: {i.password}\n\n"
        }
        data['couriers'].append(tmp)

    return render(request, "set_data.html", data)


def logt(request):
    logout(request)
    return HttpResponseRedirect('')



def courier_detail(request, date):
    try:
        formatted_date = datetime.strptime(str(date), '%Y%m%d').date()
    except:
        return HttpResponse('ERROR')
    entry = formatted_date
    shifts_on_specific_date = Couriers_shifts.objects.filter(Q(start_shift__date=entry))
    print(shifts_on_specific_date)
    data = {
        'login': f'{request.user.username}',
        'list': [],
        "data": date,
    }

    for i in shifts_on_specific_date:
        tmp = {
            "id": i.id,
            "name": i.name,
            "auto": i.auto_model,
            "number": i.auto_number,
            "where": i.where_courier
        }
        data['list'].append(tmp)

    return render(request, "courier_detail.html", data)


def courier_id(request, date, data):
    shift_id = data
    if request.method == "POST":
        print(request.POST)
        data = request.POST
        problemms = problems.objects.filter(shift_id=shift_id).all()
        for i in problemms:
            if f"ERRR-{i.id}" in data:
                print("ERROR", i)
                problem = i
                type = 2
                break
            if f"DONE-{i.id}" in data:
                print("DOONE", i)
                problem = i
                type = 1
                break

        problem.status_solving = type
        problem.comment = data['comment']
        problem.save()


    try:
        formatted_date = datetime.strptime(str(date), '%Y%m%d').date()
    except:
        print('ERROR')
        return HttpResponse("error")
    shift = Couriers_shifts.objects.filter(id=shift_id).first()
    if shift.end_shift is None:
        end = False
    else:
        end = True
    name = request.user.first_name
    print(name)
    if name is None or name == '':
        name = 'NONE'
    data = {
        'login': f'{request.user.username}',
        'table': [],
        "is_end": end,
        "manager": {
            "name": name,
            "id": request.user.id,
        },
        'courier': {
            'name': shift.name,
            'auto': shift.auto_model,
            'number': shift.auto_number,
            'where': shift.where_courier,
            'phone': shift.phone
        },
        'problem1': [],
        'problem2': []
    }


    problem = problems.objects.filter(shift_id=shift_id).all()

    for i in problem:
        client_id = i.client_id
        product = Client.objects.filter(id=client_id).first()
        if i.status_solving is None:
            solve = False
        else:
            solve = True
        if product.punkt_vidachi != 0:
            pvz_row = DictPunkt.objects.filter(id=product.punkt_vidachi).first()
            pvz = pvz_row.punkt_vidachi
        else:
            pvz = 0
        solve_status = 0
        if solve:
            solve_status = i.status_solving
        try:
            arr = i.photo.split(' ')
        except:
            arr = []
        tmp = {
            "id": i.id,
            "photo": product.img_wb,
            "article": product.article,
            "size": product.size,
            "date_buy": product.date_buy.strftime("%d.%m.%Y"),
            "phone": product.phone,
            "name": product.name,
            "price": product.price,
            "task1": product.task1,
            "pvz": pvz,
            "is_solved": solve,
            "result": solve_status,
            "photos": arr,
        }
        type_p = i.status_problem - 1
        if i.status_problem == 3:
            tmp["barcode"] = i.barcode_problem
            tmp["article"] = i.article_problem
        data[f'problem{type_p}'].append(tmp)
    print(data)

    print(shift_id)
    for_deliver = InfoDt.objects.filter(action__in=[1, 4, 5, 8], who_gave=shift_id).all()
    print()
    for i in for_deliver:
        if i.pvz != 0:
            pvz_row = DictPunkt.objects.filter(id=i.pvz).first()
            pvz = pvz_row.punkt_vidachi
        else:
            pvz = 0
        table_object = {
            "id": i.client_id,
            # "status": status_dict[int(client.status)],
            "article": i.article,
            "barcode": i.barcode,
            "clientid": i.clientid,
            "name": i.name,
            "phone": i.phone,
            "punkt_vidachi": pvz,
            "code": i.code,
            "code_qr": i.code_qr,
            "date_active": i.date_active.strftime('%Y.%m.%d'),
            "naming": i.naming,  # naming
            "task1": i.task1,
            "who_give": i.who_gave,
            "price": i.price
        }
        data['table'].append(table_object)

    return render(request, "information.html", data)


