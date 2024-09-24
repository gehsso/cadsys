from django import forms
from .models import *
import datetime
from django.core.exceptions import ValidationError



class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria']
        widgets = {
            # categoria fica oculta pq foi implementado autocomplete com jquery
            # em javascript/Funcoes.js
            # em form.html de produto o input categoria e colocado no codigo diretamente
            'categoria': forms.HiddenInput(),  # Campo oculto para armazenar o ID
            'nome':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'preco':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preço'}),
        }
        
        labels = {
            'nome': 'Nome do Produto',
            'preco': 'Preço do Produto',
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc']
        widgets = {
            'nome':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'cpf':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'C.P.F'}),
            'datanasc': forms.DateInput(attrs={'class': 'data form-control', 'placeholder': 'Data de Nascimento'}, format='%d/%m/%Y'),
        }
        


    

class MeuFormulario(forms.Form):
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Sua senha'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu e-mail'}))
    data_nascimento = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    mensagem = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    categoria = forms.ChoiceField(choices=[('1', 'Categoria 1'), ('2', 'Categoria 2'),], widget=forms.Select(attrs={'class': 'form-control'}))



class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente']
        widgets = {
            'cliente': forms.HiddenInput(),  # Campo oculto para armazenar o ID
        }
        

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['produto', 'qtde']

        widgets = {
            'produto': forms.HiddenInput(),  # Campo oculto para armazenar o ID
            'qtde':forms.TextInput(attrs={'class': 'form-control',}),
        }
    # Ajustes de formatação
    """
    def __init__(self, *args, **kwargs):
        super(ItemPedidoForm, self).__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.all()  # Lista todos os produtos disponíveis
        self.fields['qtde'].widget.attrs.update({'class': 'form-control'})  # Adiciona classe bootstrap
        self.fields['produto'].widget.attrs.update({'class': 'form-control'})  # Adiciona classe bootstrap
    """