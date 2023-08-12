from django.contrib import admin
from django.urls import path
import carrier.views


urlpatterns = [
    path('', carrier.views.main),
    path('auth', carrier.views.auth),
    path('product/<int:data>/', carrier.views.product),
    path('product/<int:data>/problem', carrier.views.problem),
]