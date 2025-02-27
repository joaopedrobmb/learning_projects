from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import ProductForm, QuotationForm
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
            
            return redirect('add_product', tracking_uuid=quotation.tracking_uuid)
            
    return render(request, 'create_quotations/quotation_form.html', {"quotation_form": quotation_form})        

def add_product(request, tracking_uuid):
    quotation = get_object_or_404(Quotation, tracking_uuid=tracking_uuid) #Busca a quotation no banco
    products = quotation.products.all() #busca todos os produtos relacionado a esta quotation no banco

    #Método POST é um tipo de solicitação HTTP utilizada para enviar dados para um servidor.
    if request.method == "POST": 
        # É criada uma instancia do formulário utilizando os dados enviados pelo método POST, que é estruturado como um dicionário
        # Estamos dizendo ao Django: "Use os dados do formulário que o usuário enviou para preencher o formulário original.
        form = ProductForm(request.POST) 
        # Após a instancia ter sido criada com os dados recebidos, é verificado se os dados estão dentro do esperado pelo formulário original.
        if form.is_valid():
            product = form.save(commit=False) #Salva o formulario do produto em product
            product.quotation = quotation # Associa o produto ao orçamento
            product.save() # Salva o produto
            
            return redirect('edit_quotation', tracking_uuid=tracking_uuid)
    else:
        form = ProductForm()
                            
    return render(request, 'create_quotations/product_form.html',
                  {"quotation": quotation,
                   "products": products,
                   "product_form": form,
                   })

def edit_quotation(request, tracking_uuid):
    #Procura um objeto Quotation no banco de dados, que id seja igual a id recebida.
    quotation = get_object_or_404(Quotation, tracking_uuid=tracking_uuid)
    products = quotation.products.all()
    
    return render(request, 'create_quotations/quotation_edit.html', {'quotation': quotation,
                                                                     'products': products})

def view_quotation(request, tracking_uuid):
    #Procura um objeto Quotation no banco de dados, que id seja igual a id recebida.
    quotation = get_object_or_404(Quotation, tracking_uuid=tracking_uuid)
    products = quotation.products.all()
    
    
    return render(request, 'create_quotations/quotation_view.html', {'quotation': quotation,
                                                                     'products': products})