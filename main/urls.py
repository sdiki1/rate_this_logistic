from django.contrib import admin
from django.urls import path
import main.views


urlpatterns = [
    path('', main.views.main),
    path('delivery/', main.views.delivery),
    path('courier/', main.views.courier),
    path('warehouse', main.views.warehouse)
]
