# Exemplos de Uso - Chatbot Theo Point Net Fibra

## Cenários de Teste Completos

Este documento apresenta exemplos práticos de como usar o Chatbot Theo, incluindo fluxos completos de conversação e casos de teste.

## Exemplo 1: Cliente Novo - Cadastro Completo

### Cenário
Um novo cliente quer se cadastrar e relatar um problema técnico.

### Fluxo de Conversação

```
🤖 Theo: Olá, seja bem-vindo(a) a Point Net Fibra, em que posso ajudar?

2) Classificação de Atendimento:
a1) Cliente novo (cadastro) ou Primeiro atendimento; ou
a2) Informações sobre planos (vendas), promoções e mudança de planos; ou
a3) Informações sobre pagamento ou débitos; ou
a4) Problemas técnicos (suporte). ou
a5) Cancelamento ou mudança de endereço.
[OBSERVAÇÃO: o cliente deverá responder apenas o termo do ítem, por exemplo, 'a.1' que quer dizer 'Cliente novo (cadastro) ou primeiro atendimento'].

👤 Cliente: a1

🤖 Theo: b1) Qual o nº de CPF do cliente (sem ponto e traço)?

👤 Cliente: 12345678901

🤖 Theo: b2) Qual o seu nome completo (sem acento)?

👤 Cliente: João Silva Santos

🤖 Theo: b3) Qual o seu telefone para contato?

👤 Cliente: 62999887766

🤖 Theo: b4) Qual a seu CEP?

👤 Cliente: 76230000

🤖 Theo: b5) Qual o seu Logradouro?

👤 Cliente: Rua das Flores

🤖 Theo: b6) Qual o seu nº da sua residência?

👤 Cliente: 123

🤖 Theo: b7) Qual o seu bairro?

👤 Cliente: Centro

🤖 Theo: b8) Existe um ponto de referência próximo a sua casa?

👤 Cliente: Próximo ao supermercado Atacadão

🤖 Theo: b9) Qual o problema/solicitação deseja realizar?

👤 Cliente: Minha internet está muito lenta, não consegue nem abrir o WhatsApp

🤖 Theo: Chamado cadastrado com sucesso! Aguarde contato de nosso suporte ou de nosso atendente.
```

### Resultado Esperado
- Cliente cadastrado em `clientes.json`
- Chamado criado em `chamados.json` com protocolo único
- Notificação enviada para equipe de suporte

## Exemplo 2: Cliente Existente - Novo Problema

### Cenário
Cliente já cadastrado quer reportar um novo problema.

### Fluxo de Conversação

```
🤖 Theo: Olá, seja bem-vindo(a) a Point Net Fibra, em que posso auxiliar?

2) Classificação de Atendimento:
a1) Cliente novo (cadastro) ou Primeiro atendimento; ou
a2) Informações sobre planos (vendas), promoções e mudança de planos; ou
a3) Informações sobre pagamento ou débitos; ou
a4) Problemas técnicos (suporte). ou
a5) Cancelamento ou mudança de endereço.
[OBSERVAÇÃO: o cliente deverá responder apenas o termo do ítem, por exemplo, 'a.1' que quer dizer 'Cliente novo (cadastro) ou primeiro atendimento'].

👤 Cliente: a4

🤖 Theo: b1) Qual o nº de CPF do cliente (sem ponto e traço)?

👤 Cliente: 12345678901

🤖 Theo: Este é você?
"nome_completo": "João Silva Santos",
"telefone": "62999887766".

👤 Cliente: sim

🤖 Theo: b9) Qual o problema/solicitação deseja realizar?

👤 Cliente: Agora a internet voltou mas o Wi-Fi não está funcionando

🤖 Theo: Chamado cadastrado com sucesso! Aguarde contato de nosso suporte ou de nosso atendente.
```

### Resultado Esperado
- Novo chamado criado para cliente existente
- Protocolo único gerado
- Dados do cliente reutilizados

## Exemplo 3: Consulta de Planos - Área Coberta

### Cenário
Cliente interessado em conhecer os planos disponíveis.

### Fluxo de Conversação

```
🤖 Theo: Olá, seja bem-vindo(a) a Point Net Fibra, em que posso ser útil?

2) Classificação de Atendimento:
a1) Cliente novo (cadastro) ou Primeiro atendimento; ou
a2) Informações sobre planos (vendas), promoções e mudança de planos; ou
a3) Informações sobre pagamento ou débitos; ou
a4) Problemas técnicos (suporte). ou
a5) Cancelamento ou mudança de endereço.
[OBSERVAÇÃO: o cliente deverá responder apenas o termo do ítem, por exemplo, 'a.1' que quer dizer 'Cliente novo (cadastro) ou primeiro atendimento'].

👤 Cliente: a2

🤖 Theo: c.1.1 - Qual o seu CPF?

👤 Cliente: 12345678901

🤖 Theo: I) Área coberta.
c.2 - Nossos Planos:
c.2.1 - Britânia/Cidade (planos abaixo [valor e plano]); ou
c.2.2 - Britânia/Fazendas (planos abaixo [valor e plano]); ou
c.2.3 - Britânia/Itacaiu (planos abaixo [valor e plano]); ou
c.2.4 - Aruanã (planos abaixo [valor e plano]); ou
c.3 - Mais informações com o Atendente humano.

👤 Cliente: c.3

🤖 Theo: Aguarde um momento por favor, estaremos direcionando seu atendimento para nossos atendentes.
```

## Exemplo 4: Consulta de Planos - Área Não Coberta

### Cenário
Cliente de área sem cobertura consulta planos.

### Fluxo de Conversação

```
🤖 Theo: Olá, seja bem-vindo(a) a Point Net Fibra, em que posso ajudar?

2) Classificação de Atendimento:
[menu de opções]

👤 Cliente: a2

🤖 Theo: c.1.1 - Qual o seu CPF?

👤 Cliente: 99999999999

🤖 Theo: c.1.2 - Qual o seu CEP?

👤 Cliente: 99999999

🤖 Theo: II) Área não coberta.
1 - Gostaria de retornar ao menu inicial? ou
2 - Gostaria de falar com um de nossos atendentes?

👤 Cliente: 2

🤖 Theo: Aguarde um momento por favor, estaremos direcionando seu atendimento para nossos atendentes.
```

## Exemplo 5: Cancelamento de Serviço

### Cenário
Cliente quer cancelar o serviço.

### Fluxo de Conversação

```
🤖 Theo: Olá, seja bem-vindo(a) a Point Net Fibra, em que posso auxiliar?

2) Classificação de Atendimento:
[menu de opções]

👤 Cliente: a5

🤖 Theo: Aguarde um momento por favor, estaremos direcionando seu atendimento para nossos atendentes.
```

## Testes via API

### Teste 1: Health Check
```bash
curl http://localhost:5000/health
```

**Resposta esperada:**
```json
{"status": "healthy"}
```

### Teste 2: Iniciar Conversa
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_001",
    "message": "ola"
  }'
```

**Resposta esperada:**
```json
{
  "status": "success",
  "response": "Olá, seja bem-vindo(a) a Point Net Fibra, em que posso auxiliar?\n\n2) Classificação de Atendimento:\na1) Cliente novo (cadastro) ou Primeiro atendimento; ou\na2) Informações sobre planos (vendas), promoções e mudança de planos; ou\na3) Informações sobre pagamento ou débitos; ou\na4) Problemas técnicos (suporte). ou\na5) Cancelamento ou mudança de endereço.\n[OBSERVAÇÃO: o cliente deverá responder apenas o termo do ítem, por exemplo, 'a.1' que quer dizer 'Cliente novo (cadastro) ou primeiro atendimento']."
}
```

### Teste 3: Fluxo de Cadastro
```bash
# Passo 1: Escolher opção a1
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_001",
    "message": "a1"
  }'

# Passo 2: Informar CPF
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_001",
    "message": "12345678901"
  }'

# Continuar com os demais passos...
```

## Casos de Teste Automatizados

### Script de Teste Python

```python
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check passou")

def test_chat_flow():
    user_id = "test_automated"
    
    # Teste 1: Iniciar conversa
    response = requests.post(f"{BASE_URL}/chat", json={
        "user_id": user_id,
        "message": "ola"
    })
    assert response.status_code == 200
    assert "Classificação de Atendimento" in response.json()["response"]
    print("✅ Inicialização passou")
    
    # Teste 2: Escolher opção a1
    response = requests.post(f"{BASE_URL}/chat", json={
        "user_id": user_id,
        "message": "a1"
    })
    assert response.status_code == 200
    assert "CPF" in response.json()["response"]
    print("✅ Seleção de opção passou")

if __name__ == "__main__":
    test_health()
    test_chat_flow()
    print("🎉 Todos os testes passaram!")
```

## Dados de Teste

### Clientes de Teste
```json
{
  "clientes": [
    {
      "id": "1",
      "cpf": "12345678901",
      "nome_completo": "João Silva Santos",
      "telefone": "62999887766",
      "enderecos": [
        {
          "cep": "76230000",
          "estado": "GO",
          "cidade": "Britânia",
          "logradouro": "Rua das Flores",
          "numero": "123",
          "bairro": "Centro",
          "complemento": "Próximo ao supermercado Atacadão"
        }
      ]
    },
    {
      "id": "2",
      "cpf": "98765432100",
      "nome_completo": "Maria Oliveira Costa",
      "telefone": "62988776655",
      "enderecos": [
        {
          "cep": "76230001",
          "estado": "GO",
          "cidade": "Britânia",
          "logradouro": "Avenida Principal",
          "numero": "456",
          "bairro": "Fazendas",
          "complemento": "Em frente à escola"
        }
      ]
    }
  ]
}
```

### Cobertura de Teste
```json
{
  "cobertura": [
    {
      "endereco_cadastrado": "Britânia Centro",
      "cidade": "Britânia",
      "bairro": "Centro",
      "cep": "76230000",
      "status": "coberto"
    },
    {
      "endereco_cadastrado": "Britânia Fazendas",
      "cidade": "Britânia",
      "bairro": "Fazendas",
      "cep": "76230001",
      "status": "coberto"
    },
    {
      "endereco_cadastrado": "Aruanã Centro",
      "cidade": "Aruanã",
      "bairro": "Centro",
      "cep": "76240000",
      "status": "coberto"
    }
  ]
}
```

## Validação de Dados

### Verificar Arquivo clientes.json
```bash
# Verificar se o arquivo existe e tem estrutura válida
cat data/clientes.json | jq .

# Contar número de clientes
cat data/clientes.json | jq '.clientes | length'

# Buscar cliente por CPF
cat data/clientes.json | jq '.clientes[] | select(.cpf == "12345678901")'
```

### Verificar Arquivo chamados.json
```bash
# Ver todos os chamados
cat data/chamados.json | jq .

# Contar chamados em aberto
cat data/chamados.json | jq '.chamados[] | select(.historico_chamados.status == "aberto") | length'

# Ver último protocolo gerado
cat data/chamados.json | jq '.chamados[-1].historico_chamados.protocolo'
```

## Monitoramento em Tempo Real

### Logs do Backend
```bash
# Seguir logs em tempo real
tail -f backend/app.log

# Filtrar apenas erros
tail -f backend/app.log | grep ERROR

# Monitorar requisições
tail -f backend/app.log | grep POST
```

### Monitoramento de Performance
```bash
# Verificar uso de CPU e memória
top -p $(pgrep -f "python app.py")

# Verificar conexões de rede
netstat -an | grep :5000

# Testar latência da API
time curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "message": "ola"}'
```

## Troubleshooting

### Problemas Comuns e Soluções

#### 1. Backend não responde
```bash
# Verificar se está rodando
ps aux | grep "python app.py"

# Verificar porta
netstat -tlnp | grep 5000

# Reiniciar
cd backend && source venv/bin/activate && python app.py
```

#### 2. Frontend não carrega
```bash
# Verificar se está rodando
ps aux | grep node

# Verificar porta
netstat -tlnp | grep 5173

# Reiniciar
cd frontend && pnpm run dev --host
```

#### 3. Dados não persistem
```bash
# Verificar permissões
ls -la data/

# Verificar estrutura JSON
cat data/clientes.json | jq .

# Corrigir se necessário
echo '{"clientes": []}' > data/clientes.json
```

#### 4. CORS errors
```bash
# Verificar se Flask-CORS está instalado
pip list | grep Flask-CORS

# Reinstalar se necessário
pip install Flask-CORS
```

---

**Última atualização**: Agosto 2025  
**Versão**: 1.0.0

