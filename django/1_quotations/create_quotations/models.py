import uuid
from django.db import models

# Create your models here.


class Quotation(models.Model):
    tracking_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    proposal_id = models.CharField(verbose_name="Código da Proposta", max_length=200, null=False, blank=False)
    quotation_version = models.CharField(auto_created=True, default="A", max_length=2, editable=False)
    client_name = models.CharField(verbose_name="Nome do Cliente", max_length=200, null=False, blank=False)
    contribution_margin = models.DecimalField(verbose_name="Margem de Contribuição(%)", max_digits=5, decimal_places=2, default=30.00, null=False, blank=False)    
    vendor_comission = models.DecimalField(verbose_name="Comissão de Venda(%)", max_digits=5, decimal_places=2, default=1.00, null=False, blank=False)    
    state = models.CharField(verbose_name="Estado da Venda", null=False, blank=False, max_length=200,
                             choices=[("MG", "Minas Gerais"),
                                      ("SP", "São Paulo")])
    
    difal_check = models.CharField(verbose_name="Difal?", null=False, blank=False, max_length=3, default="Não",
                                   choices=[("Sim", "Sim"),
                                            ("Não", "Não")])

class Product(models.Model):
    quotation = models.ForeignKey(Quotation, related_name='equipments', on_delete=models.CASCADE)
    product_type = models.IntegerField(verbose_name="Tipo do Produto", null=False, blank=False, 
                                   choices= [("TAV", "Tanque Vertical p/ Armazenamento"),
                                             ("TA", "Tanque Agitador"),
                                             ("VP", "Vaso de Pressão")])
    product_model = models.IntegerField(verbose_name="Tipo do Produto", null=False, blank=False, 
                                   choices= [("FPTE", "Fundo Plano/Tampo Elíptico"),
                                             ("FPTP", "Fundo Plano/Tampo Plano"),
                                             ("FETE", "Fundo Elíptico/Tampo Elíptico")])
    
    class Meta:
        abstract = True #Define como uma classe abstrata, não será criada uma tabela para ela.

class Tank(Product):
    diameter = models.IntegerField(verbose_name="Diâmetro Interno", null=False, blank=False, 
                                   choices= [(1000, "1000 mm"),
                                             (2500, "2500 mm")])
    
    cylindrical_length = models.IntegerField(verbose_name="Comprimento Cilíndrico",
                                             null=False, blank=False)