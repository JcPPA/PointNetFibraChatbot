import openai

chaves_api = "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"

openai.api_key = chaves_api

def enviar_mensagem (mensagem, lista_mensagens=[]):
    lista_mensagens.append(
        {"role": "user", "content": mensagem}
        )
    
    
    
    resposta = openai.ChatCompletion.create (
        model ="gpt-3.5-turbo",
        messages= lista_mensagens,
        max_tokens= 1000
    )
    
    return resposta ["choices"][0]["message"]["content"]


lista_mensagens = []

while True:
    texto = input("Digite sua mensagem: ")
    if texto.lower() == "sair":
            print("Saindo do chatbot.")
            break
    else:
            resposta = enviar_mensagem(texto, lista_mensagens)
            lista_mensagens.append(resposta)
            print("Chatbot:", resposta ["content"])
