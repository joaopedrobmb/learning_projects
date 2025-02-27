from django.contrib import admin
from django.urls import path
from create_quotations.views import view_quotation, create_quotation, quotations_list, equipments_list, add_product, edit_quotation


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', quotations_list, name='quotations_list'),
    path('create_quotation/', create_quotation, name='create_quotations'),
    path('equipments_list/<uuid:tracking_uuid>/', equipments_list, name='equipments_list'),
    path('add_product/<uuid:tracking_uuid>/', add_product, name='add_product'),
    path('edit_quotation/<uuid:tracking_uuid>/', edit_quotation, name='edit_quotation'),
    path('quotation_view/<uuid:tracking_uuid>/', view_quotation, name='quotation_view'),
]
