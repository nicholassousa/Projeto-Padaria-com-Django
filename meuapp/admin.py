from django.contrib import admin
from .models import Cliente, Pedido, Produto  # importando modelos cliente produto

# Register your models here.

admin.site.register(Cliente)  # regfistra o modelo Cliente
admin.site.register(Produto)  # retorna o modelo Pedido
admin.site.register(Pedido)  # REgsitra o modelo produto
