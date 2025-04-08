from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    primeiro_nome = models.CharField(max_length=200, default="pn_usuario{self.user.id}")
    sobre_nome = models.CharField(max_length=200, default="sn_usuario{self.user.id}")
    email = models.EmailField(max_length=200, default="email_usuario{self.user.id}")
    password = models.CharField(max_length=40)

    def __str__(self):
        return self.user.username


class Produto(models.Model):
    name = models.CharField(max_length=100)
    preço = models.DecimalField(max_digits=20, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)  # Campo para imagem do produto

    def __str__(self):
        return self.name


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.user.username} - {self.produto.name}"


class ItemCarrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    observacao = models.TextField(blank=True, null=True)  # Campo para observações do cliente

    def __str__(self):
        return f"{self.produto.name} - {self.quantidade}"