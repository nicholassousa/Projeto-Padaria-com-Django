# lembre-se de criar um arquivo urls.py dentro da pasta do app

from django.urls import path

from . import views


urlpatterns = [
    path("home/", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("registro/", views.registro, name="registro"),
    path("fazer_pedido/", views.fazer_pedido, name="fazer_pedido"),
    path("ops/", views.ops, name="ops"),
    path("carrinho/", views.carrinho, name="carrinho"),
    path("pedido_pagamento/", views.pedido_pagamento, name="pedido_pagamento"),  # Atualizado para usar a nova view
    path("visualizar_pedidos/", views.visualizar_pedidos, name="visualizar_pedidos"),
]

# lembre-se de alterar o arquivo urls.py do seu app principal (urls.py) para incluir as urls do app
