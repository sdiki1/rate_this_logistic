from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
import main.views


urlpatterns = [
    path('', main.views.main),
    path('delivery/', main.views.delivery),
    path('courier/', main.views.courier),
    path('warehouse/', main.views.warehouse),
    path('delivery/<int:date>/', main.views.delivery_detail),
    path('delivery/history', main.views.delivery_history),
    path('couriers/history', main.views.couriers_history),
    path('try/', main.views.trry),
    path('set_delivery/', main.views.set_delivery),
    path('courier/send', main.views.send_couriers),
    path('courier/send/pvz', main.views.set_pvz),
    path('courier/send/set_data', main.views.set_data),
    path('logout/', main.views.logt),
    path('couriers/<int:date>/', main.views.courier_detail),
    path('couriers/<int:date>/<int:data>/', main.views.courier_id),
    path('warehouse/get_products/', main.views.get_prod),
    path('warehouse/get_products/<int:data>/', main.views.get_product),
    path('warehouse/sort/', main.views.warehouse_sort),
    path('warehouse/sort/sorting/', main.views.warehouse_sorting)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

