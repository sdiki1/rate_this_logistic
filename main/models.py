from django.db import models
from django.contrib.auth.models import AbstractUser


class InfoProd(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.IntegerField(null=True)
    article = models.CharField(max_length=25, null=True)
    naming = models.TextField(null=True)
    barcode = models.CharField(max_length=25, null=True)
    task1 = models.BigIntegerField(null=True)
    date_last_refresh = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'info_prod'


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.IntegerField(null=True)
    status_pizdec = models.IntegerField(null=True)
    comments = models.CharField(max_length=150, null=True)
    photo = models.TextField(null=True)
    grafik = models.DateTimeField(null=True)
    mp = models.CharField(max_length=10, null=True)
    type = models.CharField(max_length=10, null=True)
    article = models.CharField(max_length=25, null=True)
    size = models.CharField(max_length=10, null=True)
    search_key = models.CharField(max_length=150, null=True)
    barcode = models.CharField(max_length=25, null=True)
    sex = models.CharField(max_length=10, null=True)
    kto_zabirat = models.TextField(null=True)
    brand = models.CharField(max_length=25, null=True)
    naming = models.TextField(null=True)
    clientid = models.CharField(max_length=25, null=True)
    name = models.CharField(max_length=25, null=True)
    surname = models.CharField(max_length=25, null=True)
    phone = models.CharField(max_length=25, null=True)
    punkt_vidachi = models.TextField(null=True)
    code_qr = models.TextField(null=True)
    code = models.CharField(max_length=50, null=True)
    date_buy = models.DateTimeField(null=True)
    date_get = models.DateField(null=True)
    order1 = models.CharField(max_length=150, null=True)
    price = models.CharField(max_length=25, null=True)
    cheque = models.CharField(max_length=500, null=True)
    rId = models.CharField(max_length=100, null=True)
    text_otziv = models.TextField(null=True)
    img_otziv = models.IntegerField(null=True)
    interval_otziv = models.IntegerField(default=240, null=True)
    screen_otziv = models.TextField(null=True)
    date_otziv = models.DateTimeField(null=True)
    in_work = models.IntegerField(default=0, null=True)
    # check = models.IntegerField(null=True)
    courier_status = models.CharField(max_length=25, null=True)
    task1 = models.BigIntegerField(null=True)
    text_wrong = models.CharField(max_length=50, null=True)
    rating_otziv = models.IntegerField(default=0, null=True)
    date_add = models.DateField(null=True)
    date_active = models.DateTimeField(null=True)
    card = models.CharField(max_length=50, null=True)
    order_id = models.CharField(max_length=50, null=True)
    group = models.CharField(max_length=255, null=True)
    img_wb = models.CharField(max_length=255, null=True)
    price_wb = models.IntegerField(null=True)
    interval_buy = models.IntegerField(null=True)
    push_telegram = models.IntegerField(default=0, null=True)
    date_set_vidacha = models.DateField(null=True)
    stop = models.IntegerField(null=True)
    #
    class Meta:
        managed = False
        db_table = 'client'


class InfoDt(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.IntegerField(null=True)
    action = models.IntegerField(null=True)
    clientid = models.CharField(max_length=25, null=True)
    date_action = models.DateTimeField(null=True)
    article = models.CharField(max_length=25, null=True)
    name = models.CharField(max_length=25, null=True)
    naming = models.CharField(max_length=255, null=True)
    date_active = models.DateTimeField(null=True)
    person = models.IntegerField(null=True)
    phone = models.CharField(max_length=25, null=True)
    barcode = models.CharField(max_length=25, null=True)
    pvz = models.IntegerField(null=True)
    code = models.CharField(max_length=25, null=True)
    code_qr = models.TextField(null=True)
    who_gave = models.CharField(max_length=50, null=True)
    date_gave = models.DateField(null=True)
    price = models.IntegerField(null=True)
    task1 = models.BigIntegerField(null=True)
    who_get = models.CharField(max_length=50, null=True)
    reason_trouble = models.TextField(null=True)
    accept_admin = models.IntegerField(null=True)
    admin_comment = models.TextField(null=True)
    brand_model_auto = models.TextField(null=True)
    who_accept = models.IntegerField(null=True)
    date_accept = models.DateField(null=True)
    who_shipped = models.IntegerField(null=True)
    date_shipped = models.DateField(null=True)

    class Meta:
        managed = True
        db_table = 'info_dt'


class DictActionsDt(models.Model):
    key = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=25, null=True)

    class Meta:
        managed = False
        db_table = 'dict_actions_dt'


class ShipProd(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.IntegerField(null=True)
    action = models.IntegerField(null=True)
    pvz = models.IntegerField(null=True)
    barcode = models.CharField(max_length=25, null=True)
    phone = models.CharField(max_length=25, null=True)
    clientid = models.CharField(max_length=25, null=True)
    person = models.IntegerField(null=True)
    date_action = models.DateTimeField(null=True)
    who_shipped = models.CharField(max_length=25, null=True)
    where_shipped = models.CharField(max_length=50, null=True)
    date_shipped = models.DateField(null=True)

    class Meta:
        managed = False
        db_table = 'ship_prod'


class Users(AbstractUser):
    # id = models.IntegerField(primary_key=True, auto_created=True)
    user_id = models.IntegerField(null=True)
    phone = models.CharField(max_length=13, null=True)
    status = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    surname = models.CharField(max_length=255, null=True)
    id_shift = models.CharField(max_length=10, null=True)
    class Meta:
        managed = True
        db_table = 'users'

class DictPunkt(models.Model):
    id = models.AutoField(primary_key=True)
    punkt_vidachi = models.CharField(max_length=255, null=True)
    mp = models.CharField(max_length=10, null=True)
    status = models.IntegerField(null=True)
    partner_status = models.IntegerField(null=True)
    partner_name = models.CharField(max_length=50, null=True)

    class Meta:
        managed = False
        db_table = 'dict_punkt'


class LastDt(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.IntegerField(null=True)
    action = models.IntegerField(null=True)
    clientid = models.CharField(max_length=25, null=True)
    date_last_action = models.DateTimeField(null=True)
    article = models.CharField(max_length=25, null=True)
    name = models.CharField(max_length=25, null=True)
    naming = models.CharField(max_length=255, null=True)
    date_active = models.DateTimeField(null=True)
    person = models.IntegerField(null=True)
    phone = models.CharField(max_length=25, null=True)
    barcode = models.CharField(max_length=25, null=True)
    pvz = models.IntegerField(null=True)
    code = models.CharField(max_length=25, null=True)
    code_qr = models.TextField(null=True)
    who_gave = models.CharField(max_length=50, null=True)
    date_gave = models.DateField(null=True)
    price = models.IntegerField(null=True)
    task1 = models.BigIntegerField(null=True)
    who_get = models.CharField(max_length=50, null=True)
    reason_trouble = models.TextField(null=True)
    accept_admin = models.IntegerField(null=True)
    admin_comment = models.TextField(null=True)
    brand_model_auto = models.TextField(null=True)
    who_accept = models.IntegerField(null=True)
    date_accept = models.DateField(null=True)
    who_shipped = models.IntegerField(null=True)
    date_shipped = models.DateField(null=True)

    class Meta:
        managed = True
        db_table = 'last_dt'


class Courier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    auto_number = models.CharField(max_length=25)
    auto_model = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, null=True)
    is_partner_now = models.IntegerField(default=1, null=True, help_text="Если курьер до сих пор сотрудничает с нами, то его статус = 1, если нет, то 0")
    class Meta:
        managed = True
        db_table = 'couriers'


class Couriers_shifts(models.Model):
    id = models.AutoField(primary_key=True)
    start_shift = models.DateTimeField(null=True)
    end_shift = models.DateTimeField(null=True)
    name = models.CharField(max_length=255)
    auto_number = models.CharField(max_length=25)
    auto_model = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, null=True)
    partner_id = models.IntegerField(null=True, help_text="Айди в таблице couriers, если этот курьер - наш партнер")
    where_courier = models.CharField(max_length=255, null=True)
    is_partner_pvz = models.IntegerField(null=False, help_text="Если 1, то только на партнерские пвз, если 2, то на непартнерские, если 0, то все")
    login = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    changed_password = models.CharField(max_length=255, null=True)
    class Meta:
        managed = True
        db_table = 'couriers_shifts'


class problems(models.Model):
    id = models.AutoField(primary_key=True)
    shift_id = models.IntegerField(null=True)
    client_id = models.IntegerField(null=True)
    status_problem = models.IntegerField(null=True)
    descriprion_problem = models.TextField(null=True)
    barcode_problem = models.CharField(max_length=50, null=True)
    article_problem = models.CharField(max_length=25, null=True)
    date_problem = models.DateTimeField(null=False)
    who_accept = models.CharField(max_length=50, null=True, help_text="Айди юзера, принявшего в работу эту проблему")
    descriprion_solving = models.TextField(null=True)
    date_solving = models.DateTimeField(null=True)
    status_solving = models.IntegerField(null=True)
    comment = models.TextField(null=True)
    photo = models.TextField(null=True, help_text="будут названия фалов, файлы хранятся в media/problem_photos/")

    class Meta:
        managed = True
        db_table = 'problems'
