from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import RegistroForm, PedidoForm, EmailAuthenticationForm
from .models import Pedido, Cliente, Produto, ItemCarrinho  # Certifique-se de importar o modelo Produto
import json


def home(request):
    return render(request, 'home.html')


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(username=email).exists():
                form.add_error('email', 'Este e-mail já está em uso.')
            else:
                user = User(
                    username=email,  # Atribui o e-mail ao campo username
                    email=email
                )
                user.set_password(form.cleaned_data['password'])
                user.save()
                Cliente.objects.create(
                    user=user,
                    primeiro_nome=form.cleaned_data['primeiro_nome'],
                    sobre_nome=form.cleaned_data['sobre_nome'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                login(request, user)
                return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # O campo 'username' contém o e-mail
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)  # Autentica usando o e-mail
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Por favor, insira um e-mail e senha corretos.')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def fazer_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = request.user.cliente
            pedido.save()
            return redirect('home')
    else:
        form = PedidoForm()
    return render(request, 'fazer_pedido.html', {'form': form})


def visualizar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'visualizar_pedidos.html', {'pedidos': pedidos})


def logout_view(request):
    logout(request)
    return redirect('home')


def pedido_pagamento(request):
    if request.method == 'POST':
        selected_products = request.POST.get('selected_products')
        payment_method = request.POST.get('payment_method')

        if selected_products:
            try:
                selected_products = json.loads(selected_products)  # Converte de JSON para lista
                produtos = Produto.objects.filter(name__in=selected_products)  # Busca os produtos no banco de dados
            except json.JSONDecodeError:
                produtos = []  # Garante que seja uma lista vazia em caso de erro
        else:
            produtos = []  # Garante que seja uma lista vazia se nenhum produto for selecionado

        if payment_method:
            # Processa o pagamento (simulação)
            return render(request, 'carrinho.html', {
                'produtos': produtos,
                'payment_method': payment_method,
                'success': True,
            })

        return render(request, 'carrinho.html', {'produtos': produtos})

    produtos = Produto.objects.all()  # Exibe todos os produtos para seleção
    return render(request, 'carrinho.html', {'produtos': produtos})


def ops(request):
    return render(request, 'ops.html')  # Redireciona para a home


def carrinho(request):
    if request.method == 'POST':
        selected_products = request.POST.getlist('selected_products')
        if selected_products:
            try:
                selected_products = json.loads(selected_products[0])  # Converte de JSON para lista
                produtos = Produto.objects.filter(name__in=selected_products)  # Busca os produtos no banco de dados
            except json.JSONDecodeError:
                produtos = []  # Garante que seja uma lista vazia em caso de erro
        else:
            produtos = []  # Garante que seja uma lista vazia se nenhum produto for selecionado

        return render(request, 'carrinho.html', {'produtos': produtos})

    return render(request, 'carrinho.html')


def carrinho_adicionar_pedido(request):
    if request.method == 'POST':
        selected_products = request.POST.getlist('selected_products')
        if selected_products:
            try:
                selected_products = json.loads(selected_products[0])  # Converte de JSON para lista
                produtos = Produto.objects.filter(name__in=selected_products)  # Busca os produtos no banco de dados
            except json.JSONDecodeError:
                produtos = []
            # Adiciona os produtos ao pedido


def carrinho_remover_produtos(request):
    if request.method == 'DELETE':
        try:
            body = json.loads(request.body)  # Converte o corpo da requisição de JSON para dicionário
            selected_product_id = body.get('product_id')  # Obtém o ID do produto a ser removido

            if selected_product_id:
                # Remove o item específico do carrinho
                ItemCarrinho.objects.filter(produto_id=selected_product_id, cliente=request.user.cliente).delete()
                return JsonResponse({'success': True, 'message': 'Produto removido com sucesso.'})
            else:
                # Informa mensagem de erro ao deletar
                return JsonResponse({'success': False, 'message': 'não foi possivel deletar o item, nenhum item foi especificado.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Erro ao processar a requisição.'}, status=400)

    return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)
