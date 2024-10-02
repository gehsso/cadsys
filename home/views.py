from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Produto, Categoria, Cliente
from .forms import *
from django.apps import apps
# Create your views here.
from django.contrib import messages


def index(request):
    return render(request,'index.html')



def form_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save()  # Salva o registro no banco de dados e retorna a instância do mesmo
            Estoque.objects.create(produto=produto, qtde=0)  # Cria um registro de estoque com quantidade inicial 0
            return redirect('produto')  # Redireciona para a listagem
    else:
        form = ProdutoForm()

    return render(request, 'produto/form.html', {'form': form})

def produto(request):
    lista_produtos = Produto.objects.all()  # Obtém todos os registros
    return render(request, 'produto/lista.html', {'lista_produtos': lista_produtos})


def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            produto = form.save()
            lista_produtos = []
            lista_produtos.append(produto) 
            return render(request, 'produto/lista.html', {'lista_produtos': lista_produtos})
    else:
         form = ProdutoForm(instance=produto)
    return render(request, 'produto/form.html', {'form': form,})

def remover_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect('produto')

def ajustar_estoque(request, id):
    produto = get_object_or_404(Produto, id=id)
    estoque = produto.estoque
    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            estoque = form.save()
            lista_produtos = []
            lista_produtos.append(estoque.produto) 
            return render(request, 'produto/lista.html', {'lista_produtos': lista_produtos})
    else:
         form = EstoqueForm(instance=estoque)
    return render(request, 'produto/estoque.html', {'form': form,})

###############################################   viewa genéricas         ###########################################

def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '')
   
    try:
        # Divida o app e o modelo
        app, modelo = app_modelo.split('.')
        modelo = apps.get_model(app, modelo)
    except LookupError:
        return JsonResponse({'error': 'Modelo não encontrado'}, status=404)
    
    # Verifica se o modelo possui os campos 'nome' e 'id'
    if not hasattr(modelo, 'nome') or not hasattr(modelo, 'id'):
        return JsonResponse({'error': 'Modelo deve ter campos "id" e "nome"'}, status=400)
    
    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)

################################### VIEWS PARA CLINTE ##################################
def cliente(request):
    lista_clientes = Cliente.objects.all().order_by('-id')
    return render(request, 'cliente/lista.html', {'lista_clientes': lista_clientes})

def form_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('cliente') 
        else:
            messages.error(request, 'Erro ao salvar o registro')
    else:
        form = ClienteForm()

    return render(request, 'cliente/form.html', {'form': form,})

def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            lista_clientes = []
            lista_clientes.append(cliente) 
            return render(request, 'cliente/lista.html', {'lista_clientes': lista_clientes})
    else:
         form = ClienteForm(instance=cliente)
    return render(request, 'cliente/form.html', {'form': form,})

def remover_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('cliente')

################################### VIEWS PARA PEDIDO ##################################
def pedido(request):
    lista_pedidos = Pedido.objects.all().order_by('-id')  # Obtém todos os registros
    return render(request, 'pedido/lista.html', {'lista_pedidos': lista_pedidos})

def novo_pedido(request,id_cliente):
    if request.method == 'GET':
        cliente = get_object_or_404(Cliente, id=id_cliente)
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)
        return render(request, 'pedido/form.html',{'form': form,})
    else:
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            return redirect('detalhar_pedido', pedido_id=pedido.id)
        


def detalhar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    # Verifica se o formulário foi enviado
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False)# retorna o objeto itempedido vindo do form
            item_pedido.pedido = pedido  # Atribui o pedido ao item
            
            # Obtém o estoque do produto relacionado
            estoqueAtual = item_pedido.produto.estoque  # Aqui você acessa o estoque do produto
            # Verifica se há quantidade suficiente
            if estoqueAtual.qtde >= item_pedido.qtde:  # Supondo que item_pedido tenha um campo quantidade
                estoqueAtual.qtde -= item_pedido.qtde
                estoqueAtual.save()  # Salva as alterações no estoque
                # Definir o preço do produto no momento da adição
                item_pedido.preco = item_pedido.produto.preco
                item_pedido.save()
                return redirect('detalhar_pedido', pedido_id=pedido_id)
            else:
                # Se não houver estoque suficiente, você pode adicionar uma mensagem de erro
                form.add_error(None, 'Quantidade em estoque insuficiente para o pedido.')

    # Método GET
    else:
        form = ItemPedidoForm()

    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/detalhes.html',contexto )


def editar_item_pedido(request, item_id):
    item_pedido = get_object_or_404(ItemPedido, id=item_id)
    pedido = item_pedido.pedido  # Acessa o pedido diretamente do item
    quantidade_anterior = item_pedido.qtde  # Armazena a quantidade anterior
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            item_pedido = form.save(commit=False)  # Salva a instância do item_pedido sem persistir ainda
            nova_quantidade = item_pedido.qtde  # A nova quantidade do item pedido

            estoque = item_pedido.produto.estoque  # Obtém o estoque do produto

            # Verifica se há estoque suficiente para a nova quantidade
            if (estoque.qtde + quantidade_anterior) >= nova_quantidade:
                # Retorna a quantidade anterior ao estoque
                estoque.qtde += quantidade_anterior
                estoque.save()  # Salva as alterações no estoque

                estoque.qtde -= nova_quantidade  # Decrementa a nova quantidade do estoque
                estoque.save()  # Salva as alterações no estoque

                # Salva o item do pedido após ajustar o estoque
                item_pedido.save()  # Agora salva a instância de item_pedido
                return redirect('detalhar_pedido', pedido_id=pedido.id)
            else:
                form.add_error(None, 'Quantidade em estoque insuficiente para o produto.')
                return render(request, 'pedido/detalhes.html', {'pedido': pedido, 'form': form, 'item_pedido': item_pedido})
    else:
        form = ItemPedidoForm(instance=item_pedido)
        

    contexto = {
        'pedido': pedido,
        'form': form,
        'item_pedido': item_pedido,
    }
    return render(request, 'pedido/detalhes.html', contexto)



def remover_item_pedido(request, item_id):
    item_pedido = get_object_or_404(ItemPedido, id=item_id)
    pedido_id = item_pedido.pedido.id  # Armazena o ID do pedido antes de remover o item
    estoque = item_pedido.produto.estoque  # Obtém o estoque do produto
    estoque.qtde += item_pedido.qtde  # Devolve a quantidade do item ao estoque
    estoque.save()  # Salva as alterações no estoque
    # Remove o item do pedido
    item_pedido.delete()

    # Redireciona de volta para a página de detalhes do pedido
    return redirect('detalhar_pedido', pedido_id=pedido_id)

def remover_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    
    # Itera sobre os itens do pedido
    for item_pedido in pedido.itempedido_set.all():
        estoque = item_pedido.produto.estoque  # Obtém o estoque do produto
        estoque.qtde += item_pedido.qtde  # Devolve a quantidade do item ao estoque
        estoque.save()  # Salva as alterações no estoque
        messages.success(request, 'Operação realizada com Sucesso')

            
    pedido.delete()
    return redirect('pedido')

def form_pagamento(request,id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o objeto no banco de dados e retorna a instância do mesmo
            return redirect('detalhar_pedido', pedido_id=pedido.id)
    else:
        
        form = PagamentoForm()

    return render(request, 'pedido/pagamento.html', {'form': form})

def form_pagamento(request,id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            form.save()
    
    pagamento = Pagamento(pedido=pedido)
    form = PagamentoForm(instance=pagamento)
        
    contexto = {
        'pedido': pedido,
        'form': form,
    }    
        
    return render(request, 'pedido/pagamento.html',contexto)


def editar_pagamento(request, id):
    pagamento = get_object_or_404(Pagamento, id=id)
    pedido = pagamento.pedido
    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            pagamento = form.save()
            messages.success(request, 'Operação realizada com Sucesso')

   
    else:#GET
        form = PagamentoForm(instance=pagamento)

    contexto = {
        'pedido': pedido,
        'form': form,
    }    
        
    return render(request, 'pedido/pagamento.html',contexto)

def remover_pagamento(request, id):
    pagamentoRemover = get_object_or_404(Pagamento, id=id)
    pedido = pagamentoRemover.pedido
    pagamentoRemover.delete()
    pagamento = Pagamento(pedido=pedido)
    form = PagamentoForm(instance=pagamento)
    contexto = {
        'pedido': pedido,
        'form': form,
    }    
    return render(request, 'pedido/pagamento.html',contexto)



###################################TESTE AJUSTE PREÇO #################################