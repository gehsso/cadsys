# utils/context_processors.py
from datetime import datetime

def data_atual(request):
    return {
        'data_atual': datetime.now()
    }
    
    
def formatar_moeda(valor):
    """
    Formata o valor como moeda brasileira (R$).
    :param valor: Valor numérico a ser formatado
    :return: String formatada no padrão brasileiro de moeda
    """
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Para usar a função nos templates, é necessário expô-la como um context processor
def moeda_processor(request):
    return {
        'formatar_moeda': formatar_moeda
    }    