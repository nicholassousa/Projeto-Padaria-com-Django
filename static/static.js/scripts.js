document.addEventListener('DOMContentLoaded', function() {
    // Seleciona todas as caixas de produtos na página home
    const productBoxes = document.querySelectorAll('.product-box');

    productBoxes.forEach(box => {
        box.addEventListener('click', function() {
            // Verifica se a classe 'active' já está presente
            if (this.classList.contains('active')) {
                // Remove a classe 'active' se já estiver presente
                this.classList.remove('active');
            } else {
                // Adiciona a classe 'active' ao elemento clicado
                this.classList.add('active');
            }
        });
    });

    const paymentButton = document.querySelector('.header-button[type="submit"]');
    paymentButton.addEventListener('click', function(event) {
        event.preventDefault();

        if (selectedProducts.length === 0) {
            alert('Por favor, selecione pelo menos um produto antes de prosseguir.');
            return;
        }

        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/pedido_pagamento/'; // Certifique-se de que a URL está correta

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        form.appendChild(csrfInput);

        const selectedInput = document.createElement('input');
        selectedInput.type = 'hidden';
        selectedInput.name = 'selected_products';
        selectedInput.value = JSON.stringify(selectedProducts);
        form.appendChild(selectedInput);

        document.body.appendChild(form);
        form.submit();
    });
});
