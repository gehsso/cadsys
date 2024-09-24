from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Produto, Categoria, Cliente
from .forms import *
from django.apps import apps
# Create your views here.


def index(request):
    return render(request,'index.html')

def user(request):
    form = MeuFormulario()
    return render(request,'user/lista.html',{'form': form})

def form_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produto')  # Redireciona para a lista de produtos ou outra página desejada
    else:
        form = ProdutoForm()

    return render(request, 'produto/form.html', {'form': form})

def produto(request):
    produtos = Produto.objects.all()  # Obtém todos os produtos
    return render(request, 'produto/lista.html', {'produtos': produtos})


def buscar_categorias(request):
    termo = request.GET.get('q', '')
    categorias = Categoria.objects.filter(nome__icontains=termo)
    resultados = [{'id': categoria.id, 'nome': categoria.nome} for categoria in categorias]
    return JsonResponse(resultados, safe=False)

def listar_produtos(request):
    produtos = Produto.objects.all()
    produtos_data = [{'nome': produto.nome, 'preco': produto.preco_formatado, 'categoria': produto.categoria.nome} for produto in produtos]
    return JsonResponse(produtos_data, safe=False)


def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '')
    
    try:
        # Divida o app e o modelo
        app_label, model_name = app_modelo.split('.')
        modelo = apps.get_model(app_label, model_name)
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
    lista = Cliente.objects.all()  # Obtém todos os registros
    return render(request, 'cliente/lista.html', {'lista': lista})

def form_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente')  
    else:
        form = ClienteForm()

    return render(request, 'cliente/form.html', {'form': form})

################################### VIEWS PARA CLINTE ##################################
def pedido(request):
    lista = Pedido.objects.all()  # Obtém todos os registros
    return render(request, 'pedido/lista.html', {'lista': lista})

def novo_pedido(request,id_cliente):
    if request.method == 'GET':
        cliente = get_object_or_404(Cliente, id=id_cliente)
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)
        contexto = {
            'form':form,
        }
        
        return render(request, 'pedido/form.html',contexto)
    else:
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedido')
        


def detalhar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    # Verifica se o formulário foi enviado
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False)# retorna o objeto itempedido vindo do form
            item_pedido.pedido = pedido  # Atribui o pedido ao item
            # Definir o preço do produto no momento da adição
            item_pedido.preco = item_pedido.produto.preco
            item_pedido.save()
            return redirect('detalhar_pedido', pedido_id=pedido_id)
    else:
        form = ItemPedidoForm()

    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/detalhes.html',contexto )

