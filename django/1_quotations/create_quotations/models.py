import uuid
from django.db import models
from create_quotations.calc_module.utils import math, data_loader

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
    quotation = models.ForeignKey(Quotation, related_name='products', on_delete=models.CASCADE)
    product_type = models.CharField(verbose_name="Tipo", null=False, blank=False, max_length=200, 
                                   choices= [("TA", "Tanque para Armazenamento"),
                                             ("TA", "Tanque Agitador"),
                                             ("VP", "Vaso de Pressão"),
                                             ("SE", "Serviço")])
    product_model = models.CharField(verbose_name="Modelo", null=False, blank=False, max_length=200, 
                                   choices= [("FPTE", "Fundo Plano/Tampo Elíptico"),
                                             ("FPTP", "Fundo Plano/Tampo Plano"),
                                             ("FETE", "Fundo Elíptico/Tampo Elíptico"),
                                             ("MAN", "Manutenção" )])
    
    class Meta:
        abstract = True #Define como uma classe abstrata, não será criada uma tabela para ela.

class Tank(Product):
    diameter = models.IntegerField(verbose_name="Diâmetro Interno", null=False, blank=False, 
                                   choices= [(1000, "1000 mm"),
                                             (2500, "2500 mm")])
    cylindrical_length = models.IntegerField(verbose_name="Comprimento Cilíndrico",
                                             null=False, blank=False)
    volume = models.IntegerField(verbose_name="Volume", null=True, blank=True)
    
    def calculate_volume(self):
        return round(math.calculate_volume_tank(self.diameter, self.cylindrical_length), 2)
    
    def save(self, *args, **kwargs):
        """Sobrescreve o método save para calcular o volume automaticamente"""
        self.volume = self.calculate_volume()  # Calcula o volume e atribui ao campo
        super().save(*args, **kwargs)  # Salva a instância no banco de dados