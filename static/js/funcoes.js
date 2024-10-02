function autoComplete(inputSelector) {
    // Obtemos a URL e o seletor do campo hidden dos atributos data-url e data-hidden do input
    var inputElement = $(inputSelector);
    var buscaUrl = inputElement.data('url');
    var hiddenSelector = inputElement.data('hidden');

    $(inputSelector).autocomplete({
        source: function(request, response) {
            $.ajax({
                url: buscaUrl,  // URL obtida do atributo data-url
                dataType: "json",
                data: {
                    q: request.term  // O termo digitado no campo de entrada
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item.nome,  // O que será exibido na lista
                            value: item.nome,  // O valor que será preenchido no campo de entrada
                            id: item.id        // O ID que será preenchido no campo hidden
                        };
                    }));
                }
            });
        },
        select: function(event, ui) {
            $(hiddenSelector).val(ui.item.id);  // Atualiza o campo hidden com o ID selecionado
        }
    });
}
