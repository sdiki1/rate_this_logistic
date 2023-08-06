from django.contrib import admin
from django.urls import path
import main.views


urlpatterns = [
    path('', main.views.main),
    path('delivery/', main.views.delivery),
    path('courier/', main.views.courier),
    path('warehouse/', main.views.warehouse),
    path('delivery/<int:date>/', main.views.delivery_detail, name='delivery_detail'),
    path('delivery/history', main.views.delivery_history),
    path('couriers/history', main.views.couriers_history),
    path('try/', main.views.trry)
]
