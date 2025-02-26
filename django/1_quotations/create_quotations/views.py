from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import EquipmentForm, QuotationForm
from .models import Quotation

def quotations_list(request):
    quotations = Quotation.objects.all() #Pega todas as quotations do banco;
    
    return render(request, 'create_quotations/quotations_list.html', {"quotations": quotations})

def equipments_list(request, tracking_uuid):
    quotation = get_object_or_404(Quotation, tracking_uuid=tracking_uuid)
    
    equipments = quotation.equipments.all()
    
    return render(request, 'create_quotations/equipments_list.html', 
                  {"quotation": quotation,
                   "equipments": equipments})

def create_quotation(request):
    quotation_form = QuotationForm()
    
    if request.method == "POST":
        quotation_form = QuotationForm(request.POST)
        if quotation_form.is_valid():
            quotation = quotation_form.save()
            
            return redirect('equipments_list', tracking_uuid=quotation.tracking_uuid)
            
    return render(request, 'create_quotations/quotation_form.html', {"quotation_form": quotation_form})        
    

def create_equipment(request):
    equipament_form = EquipmentForm()
    
    #Método POST é um tipo de solicitação HTTP utilizada para enviar dados para um servidor.
    if request.method == "POST": 
        # É criada uma instancia do formulário utilizando os dados enviados pelo método POST, que é estruturado como um dicionário
        # Estamos dizendo ao Django: "Use os dados do formulário que o usuário enviou para preencher o formulário original.
        equipament_form = EquipmentForm(request.POST) 
        # Após a instancia ter sido criada com os dados recebidos, é verificado se os dados estão dentro do esperado pelo formulário original.
        if equipament_form.is_valid():
            # Se for validado, o formulário é salvo no banco de dados.
            equipament_form.save()
                            
    return render(request, 'create_quotations/equipment_form.html', {"equipament_form": equipament_form})

def view_quotation(request, tracking_uuid):
    #Procura um objeto Quotation no banco de dados, que id seja igual a id recebida.
    quotation = get_object_or_404(Quotation, tracking_uuid=tracking_uuid)
    
    return render(request, 'create_quotations/quotation_view.html', {'quotation': quotation})