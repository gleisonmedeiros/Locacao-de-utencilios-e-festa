from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ProdutoForm, ClienteForm, PedidoModelForm,ItemPedidoForm
from .models import Cliente_Model, Produto_Model
from .models import PedidoModel, ItemPedido
from collections import defaultdict
from datetime import datetime
import locale
from unidecode import unidecode

locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8')

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
    if request.method == 'GET':

        produtos_por_cliente = defaultdict(list)

        # Consulta para obter os itens dos pedidos com informações relacionadas
        pedidos_itens = ItemPedido.objects.select_related('produto', 'pedido__cliente').all()

        # Preencher o dicionário com os produtos agrupados por cliente
        for pedido_item in pedidos_itens:
            produto_nome = pedido_item.produto
            quantidade_alugada = pedido_item.quantidade_alugada
            cliente_nome = pedido_item.pedido.cliente

            data = pedido_item.pedido.data_de_locacao
            data_formatada = datetime.strptime(data, "%d/%m/%Y")
            # Obtenha o nome do dia da semana
            #print((data_formatada.strftime("%A")))
            dia_da_semana = unidecode((data_formatada.strftime("%A").capitalize()))
            if (dia_da_semana == 'Sa!bado'):
                dia_da_semana = 'Sábado'
            data_locacao =data + ' - ' + dia_da_semana
            local=(pedido_item.pedido.local)
            observacao = (pedido_item.pedido.observacao)
            chave = (cliente_nome, data_locacao,local,observacao)

            # Adicionar informações ao dicionário
            produtos_por_cliente[chave].append({
                'produto_nome': produto_nome,
                'quantidade_alugada': quantidade_alugada,
            })

        dicionario_novo = dict(produtos_por_cliente)

        result = []
        for chave, items in dicionario_novo.items():
            cliente_nome, data_locacao,local,observacao = chave  # Desempacotando a tupla
            result.append((cliente_nome, data_locacao,local,observacao,
                           [[item['produto_nome'], item['quantidade_alugada']] for item in items]))

        # Exibindo a lista de resultados
        #print(result)

        # Criando a lista de dados para renderizar no template
        lista_dados = [(nome, data,local,observacao, itens) for nome, data,local,observacao, itens in result]

        return render(request, 'agenda.html', {'lista_dados': lista_dados})


    elif request.method == 'POST':

        if 'delete_itens' in request.POST:
            nome_cliente = (request.POST['nome'].split(' - ')[0])
            data = (request.POST['data'].split(' ')[0])
            print(nome_cliente)
            print(data)
            cliente = Cliente_Model.objects.get(nome=nome_cliente)  # Obtenha o objeto do cliente pelo nome
            pedido = PedidoModel.objects.get(cliente=cliente,data_de_locacao=data)  # Consulte o pedido usando o objeto do cliente
            pedido.delete()
            return redirect('agenda')



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
    pedido = PedidoModel(cliente=cliente, data_de_locacao=lista2[0][4],local=lista2[0][5],observacao=lista2[0][6])

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
            try:

                if form.is_valid():
                    # Salvar pedido principal
                    pedido = form.cleaned_data.get('cliente')
                    data = form.cleaned_data.get('data_de_locacao')
                    local = form.cleaned_data.get('local')
                    observacao = form.cleaned_data.get('observacao')
                    nova_data = str(data)

                    # Salvar itens do pedido
                    itens_pedido_formset = form.itens_pedido(queryset=ItemPedido.objects.none(), data=request.POST)
                    if itens_pedido_formset.is_valid():

                        for formset_form in itens_pedido_formset:
                            produto = formset_form.cleaned_data.get('produto')
                            quantidade_alugada = formset_form.cleaned_data.get('quantidade_alugada')
                            texto = (str(pedido))
                            nome = texto.split(" - ")[0]
                            lista = [nome,produto.nome,produto.modelo,quantidade_alugada,nova_data,local,observacao]
                        lista2.append(lista)

                        return render(request, 'cadastro_pedido.html', {'form': form})  # Redirecionar para a página de sucesso após salvar
                    else:
                        print("Formulário do item não é válido")
            except:
                print("Erro ao salvar o Item")
            else:
                print("Formulário principal não é válido")

        elif 'save_pedido' in request.POST:
            try:
                salva_pedido()

                resultado = 1
            except:
                resultado = 0

            form = PedidoModelForm()
            contexto = {'form': form,'resultado':resultado}
            lista2 = []

            return render(request, 'cadastro_pedido.html', contexto)
    else:
        form = PedidoModelForm()

    return render(request, 'cadastro_pedido.html', {'form': form})