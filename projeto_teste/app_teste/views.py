from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ProdutoForm, ClienteForm, PedidoModelForm,ItemPedidoForm
from .models import Cliente_Model, Produto_Model
from .models import PedidoModel, ItemPedido


def ola_mundo(request):
    return HttpResponse("Ola mundo!")

def index(request):
    return render(request, 'index.html')

def cadastro_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            form = ClienteForm()
            dicionario = {'form': form, 'sucesso': 1}
            return render(request, 'cadastro_cliente.html', dicionario)
        else:
            dicionario = {'form': form, 'sucesso': 0}
            return render(request, 'cadastro_cliente.html', dicionario)
    else:
        form = ClienteForm()
    return render(request, 'cadastro_cliente.html', {'form': form})


def agenda(request):
    return render(request, 'agenda.html')

def cadastro_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            form = ProdutoForm()
            dicionario = {'form': form, 'sucesso': 1}
            return render(request, 'cadastro_produto.html', dicionario)
        else:
            dicionario = {'form': form, 'sucesso': 0}
            return render(request, 'cadastro_produto.html', dicionario)
    else:
        form = ProdutoForm()
    return render(request, 'cadastro_produto.html', {'form': form})


def cadastro_pedido(request):
    itens_acumulados = []

    form = PedidoModelForm(request.POST or None)

    if request.method == 'POST':
        if 'save_itens' in request.POST:
            print("iu")
            # Criar uma instância do cliente (substitua 'nome_do_cliente' pelo nome real)
            cliente = Cliente_Model.objects.get(nome='romeu')

            # Criar uma instância do pedido
            pedido = PedidoModel(cliente=cliente)
            pedido.save()

            # Adicionar itens ao pedido
            produto1 = Produto_Model.objects.get(nome='cadeira')
            item1 = ItemPedido(produto=produto1, quantidade_alugada=2, pedido=pedido)
            item1.save()

            produto2 = Produto_Model.objects.get(nome='mesa')
            item2 = ItemPedido(produto=produto2, quantidade_alugada=3, pedido=pedido)
            item2.save()


        elif 'save_pedido' in request.POST:
            # Botão para salvar o pedido pressionado
            if form.is_valid():
                pedido = form.save()
                # Adicione os itens acumulados ao pedido
                for item_acumulado in itens_acumulados:
                    item_acumulado.pedido = pedido
                    item_acumulado.save()

                return redirect('cadastro_pedido')

    return render(request, 'cadastro_pedido.html', {'form': form})