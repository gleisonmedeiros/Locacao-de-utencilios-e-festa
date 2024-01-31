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

'''
def cadastro_pedido(request):
    itens_acumulados = []

    form = PedidoModelForm(request.POST or None)


    if request.method == 'POST':
        if 'save_itens' in request.POST:
            if form.is_valid():
                cliente = form.cleaned_data['cliente']
                print(f'Cliente: {cliente}')

                # Acesso aos dados do formset
                itens_pedido_formset = form.itens_pedido(queryset=ItemPedido.objects.none(), data=request.POST)

                # Verificar se o formset é válido
                if itens_pedido_formset.is_valid():
                    for formset_form in itens_pedido_formset:
                        produto = formset_form.cleaned_data.get('produto')
                        quantidade_alugada = formset_form.cleaned_data.get('quantidade_alugada')
                        if produto and quantidade_alugada:
                            print(f'Produto: {produto}, Quantidade Alugada: {quantidade_alugada}')
                else:
                    print("Formulário não é válido")

                # Adicione lógica adicional conforme necessário

            else:
                print("erro no formulário")

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
'''

def salva_pedido():
    # Criar uma instância do cliente (substitua 'nome_do_cliente' pelo nome real)
    for lista in lista2:

        cliente = Cliente_Model.objects.get(nome=lista[0])

        # Criar uma instância do pedido
        pedido = PedidoModel(cliente=cliente)
        pedido.save()

        # Adicionar itens ao pedido
        produto1 = Produto_Model.objects.get(nome=lista[1],modelo=lista[2])
        item1 = ItemPedido(produto=produto1, quantidade_alugada=lista[3], pedido=pedido)
        item1.save()

        '''
        produto2 = Produto_Model.objects.get(nome=lista[2])
        item2 = ItemPedido(produto=produto2, quantidade_alugada=3, pedido=pedido)
        item2.save()
        '''

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
                        print(pedido)
                        print(produto)
                        print(quantidade_alugada)
                        lista = [pedido.cliente.nome,produto.nome,produto.modelo,quantidade_alugada]
                    lista2.append(lista)
                    print(lista2)
                    '''

                    if produto and quantidade_alugada:
                        item_pedido = formset_form.save(commit=False)
                        item_pedido.pedido = pedido  # Certifique-se de associar ao pedido
                        item_pedido.save()

                    '''
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