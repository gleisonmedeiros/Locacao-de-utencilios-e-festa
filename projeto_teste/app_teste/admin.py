from django.contrib import admin
from .models import Cliente_Model, Produto_Model, Pedido_Model

# Register your models here.
@admin.register(Cliente_Model)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telefone', 'cep', 'estado', 'cidade', 'endereco', 'numero', 'referencia']

@admin.register(Produto_Model)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'modelo', 'quantidade']

@admin.register(Pedido_Model)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'data_locacao', 'observacoes']
    filter_horizontal = ['produtos']  # Isso torna o campo produtos mais amigável para múltipla escolha no admin