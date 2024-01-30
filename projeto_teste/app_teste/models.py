from django.db import models

class Produto_Model(models.Model):
    nome = models.CharField(max_length=80)
    modelo = models.CharField(max_length=80)
    quantidade = models.IntegerField()

    def __str__(self):
        return f'{self.nome} - {self.modelo}'

class Cliente_Model(models.Model):
    nome = models.CharField(max_length=80)
    telefone = models.CharField(max_length=80)
    cep = models.CharField(max_length=10)
    estado = models.CharField(max_length=20)
    cidade = models.CharField(max_length=60)
    endereco = models.CharField(max_length=100)
    numero = models.IntegerField()
    referencia = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class PedidoModel(models.Model):
    cliente = models.ForeignKey(Cliente_Model, on_delete=models.CASCADE)
    itens_pedido = models.ManyToManyField('ItemPedido',blank=True, null=True)  # Use aspas para evitar referência circular

    def __str__(self):
        return f"{self.cliente.nome}'s Pedido"

class ItemPedido(models.Model):
    produto = models.ForeignKey(Produto_Model, on_delete=models.CASCADE)
    quantidade_alugada = models.IntegerField()
    pedido = models.ForeignKey(PedidoModel, on_delete=models.CASCADE)  # Adiciona a chave estrangeira para Pedido_Model

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade_alugada}"