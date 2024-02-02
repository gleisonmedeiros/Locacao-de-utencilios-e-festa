from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ProdutoForm, ClienteForm, PedidoModelForm,ItemPedidoForm
from .models import Cliente_Model, Produto_Model
from .models import PedidoModel, ItemPedido
from collections import defaultdict

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
    produtos_por_cliente = defaultdict(list)

    # Consulta para obter os itens dos pedidos com informações relacionadas
    pedidos_itens = ItemPedido.objects.select_related('produto', 'pedido__cliente').all()

    # Preencher o dicionário com os produtos agrupados por cliente
    for pedido_item in pedidos_itens:
        produto_nome = pedido_item.produto.nome
        quantidade_alugada = pedido_item.quantidade_alugada
        cliente_nome = pedido_item.pedido.cliente.nome

        # Adicionar informações ao dicionário
        produtos_por_cliente[cliente_nome].append({
            'produto_nome': produto_nome,
            'quantidade_alugada': quantidade_alugada,
        })

    # Criar um contexto com os dados a serem enviados para o template

    return render(request, 'agenda.html',{'produtos_por_cliente': produtos_por_cliente})

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