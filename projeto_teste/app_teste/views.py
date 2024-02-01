from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ProdutoForm, ClienteForm, PedidoModelForm,ItemPedidoForm
from .models import Cliente_Model, Produto_Model
from .models import PedidoModel, ItemPedido

lista2 = []


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
    pedidos = PedidoModel.objects.select_related('cliente').prefetch_related('itens_pedido')

    # Crie um dicionário para armazenar os itens do pedido agrupados por cliente
    itens_por_cliente = {}

    # Agrupe os itens do pedido por cliente
    for pedido in pedidos:
        cliente = pedido.cliente

        # Se o cliente ainda não estiver no dicionário, crie uma lista vazia para ele
        if cliente not in itens_por_cliente:
            itens_por_cliente[cliente] = []

        # Adicione os itens do pedido à lista do cliente
        itens_por_cliente[cliente].extend(pedido.itens_pedido.all())

    # Imprima os detalhes no console para cada cliente
    for cliente, itens_cliente in itens_por_cliente.items():
        print(f"Cliente: {cliente.nome}")

        # Imprima os detalhes do item para cada cliente
        for item_pedido in itens_cliente:
            print(f"  Produto: {item_pedido.produto.nome}")
            print(f"  Quantidade Alugada: {item_pedido.quantidade_alugada}")

        print("-" * 20)  # Linha separadora opcional
    return render(request, 'agenda.html',{})

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


def salva_pedido():
    global lista2

    cliente = Cliente_Model.objects.get(nome=lista2[0][0])
    pedido = PedidoModel(cliente=cliente)
    pedido.save()
    # Criar uma instância do cliente (substitua 'nome_do_cliente' pelo nome real)
    for lista in lista2:

        # Adicionar itens ao pedido
        produto1 = Produto_Model.objects.get(nome=lista[1],modelo=lista[2])
        item1 = ItemPedido(produto=produto1, quantidade_alugada=lista[3], pedido=pedido)
        item1.save()


def cadastro_pedido(request):
    global lista2
    if request.method == 'POST':
        form = PedidoModelForm(request.POST)
        if 'save_itens' in request.POST:

            if form.is_valid():
                # Salvar pedido principal
                pedido = form.cleaned_data.get('cliente')

                # Salvar itens do pedido
                itens_pedido_formset = form.itens_pedido(queryset=ItemPedido.objects.none(), data=request.POST)
                if itens_pedido_formset.is_valid():

                    for formset_form in itens_pedido_formset:
                        produto = formset_form.cleaned_data.get('produto')
                        quantidade_alugada = formset_form.cleaned_data.get('quantidade_alugada')
                        nome = (str(pedido))
                        lista = [nome,produto.nome,produto.modelo,quantidade_alugada]
                    lista2.append(lista)
                    print(lista2)

                    return render(request, 'cadastro_pedido.html', {'form': form})  # Redirecionar para a página de sucesso após salvar
                else:
                    print("Formulário do item não é válido")
            else:
                print("Formulário principal não é válido")

        elif 'save_pedido' in request.POST:
            salva_pedido()
            lista2 = []
    else:
        form = PedidoModelForm()

    return render(request, 'cadastro_pedido.html', {'form': form})