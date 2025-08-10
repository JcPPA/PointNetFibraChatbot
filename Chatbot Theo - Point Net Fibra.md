# Chatbot Theo - Point Net Fibra

## Visão Geral

O Chatbot Theo é um sistema de atendimento automatizado desenvolvido especificamente para a Point Net Fibra, uma empresa de telecomunicações. Este sistema foi projetado para realizar triagem automática de solicitações, aprender com interações através de machine learning, otimizar o fluxo de atendimento via WhatsApp e gerar registros estruturados para análise futura.

## Características Principais

### Funcionalidades Implementadas

- **Saudação Inteligente**: O chatbot adapta sua mensagem de boas-vindas baseada no horário do dia (matutino, vespertino ou noturno)
- **Classificação de Atendimento**: Sistema de triagem que direciona clientes para diferentes fluxos baseado em suas necessidades
- **Gestão de Clientes**: Cadastro e busca de clientes com validação de CPF
- **Sistema de Chamados**: Criação e gerenciamento de protocolos de atendimento
- **Verificação de Cobertura**: Validação de disponibilidade de serviços por localização
- **Interface Web Moderna**: Frontend React responsivo e intuitivo

### Tecnologias Utilizadas

- **Backend**: Flask (Python 3.11)
- **Frontend**: React com Vite
- **Banco de Dados**: Arquivos JSON para persistência
- **Estilização**: Tailwind CSS com shadcn/ui
- **APIs**: Preparado para integração com WhatsApp (WAHA) e OpenAI

## Estrutura do Projeto

```
chatbot_pointnet/
├── backend/
│   ├── venv/                 # Ambiente virtual Python
│   ├── app.py               # Aplicação Flask principal
│   └── requirements.txt     # Dependências Python
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── App.jsx         # Componente principal
│   │   └── App.css         # Estilos
│   ├── package.json        # Dependências Node.js
│   └── index.html          # Página HTML principal
└── data/
    ├── clientes.json       # Base de dados de clientes
    ├── chamados.json       # Base de dados de chamados
    └── cobertura.json      # Base de dados de cobertura
```

## Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- Node.js 20.x ou superior
- pnpm (gerenciador de pacotes)

### Configuração do Backend

1. **Navegue para o diretório do backend**:
   ```bash
   cd chatbot_pointnet/backend
   ```

2. **Crie e ative o ambiente virtual**:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o servidor**:
   ```bash
   python app.py
   ```

O backend estará disponível em `http://localhost:5000`

### Configuração do Frontend

1. **Navegue para o diretório do frontend**:
   ```bash
   cd chatbot_pointnet/frontend
   ```

2. **Instale as dependências**:
   ```bash
   pnpm install
   ```

3. **Execute o servidor de desenvolvimento**:
   ```bash
   pnpm run dev --host
   ```

O frontend estará disponível em `http://localhost:5173`

## Fluxos de Atendimento

### 1. Saudação Inicial

O chatbot inicia a conversa com uma mensagem personalizada baseada no horário:

- **06:00 às 12:30**: "Olá, seja bem-vindo(a) a Point Net Fibra, em que posso ajudar?"
- **12:31 às 18:30**: "Olá, seja bem-vindo(a) a Point Net Fibra, em que posso ser útil?"
- **18:31 às 05:59**: "Olá, seja bem-vindo(a) a Point Net Fibra, em que posso auxiliar?"

### 2. Classificação de Atendimento

Após a saudação, o sistema apresenta as opções:

- **a1**: Cliente novo (cadastro) ou Primeiro atendimento
- **a2**: Informações sobre planos (vendas), promoções e mudança de planos
- **a3**: Informações sobre pagamento ou débitos
- **a4**: Problemas técnicos (suporte)
- **a5**: Cancelamento ou mudança de endereço

### 3. Fluxo de Cadastro (a1 e a4)

Para clientes novos ou problemas técnicos, o sistema coleta:

1. **CPF** (validação e busca na base)
2. **Nome completo** (se não encontrado)
3. **Telefone para contato**
4. **CEP**
5. **Logradouro**
6. **Número da residência**
7. **Bairro**
8. **Ponto de referência**
9. **Descrição do problema/solicitação**

### 4. Fluxo de Planos (a2)

Para informações sobre planos:

1. **Verificação de CPF** ou **CEP**
2. **Validação de cobertura**
3. **Apresentação de planos disponíveis** por região
4. **Opção de atendimento humano**

### 5. Encaminhamento para Atendente (a5)

Direciona automaticamente para atendimento humano com notificação.

## API Endpoints

### Backend Flask

#### POST /chat
Endpoint principal para interação com o chatbot.

**Parâmetros**:
```json
{
  "user_id": "string",
  "message": "string"
}
```

**Resposta**:
```json
{
  "status": "success",
  "response": "string"
}
```

#### POST /webhook
Endpoint para integração com WhatsApp (WAHA).

#### GET /health
Endpoint de verificação de saúde do sistema.

## Estrutura dos Dados

### clientes.json
```json
{
  "clientes": [
    {
      "id": "1",
      "cpf": "12345678901",
      "nome_completo": "João Silva",
      "telefone": "62999999999",
      "enderecos": [
        {
          "cep": "76230000",
          "estado": "GO",
          "cidade": "Britânia",
          "logradouro": "Rua Principal",
          "numero": "123",
          "bairro": "Centro",
          "complemento": "Próximo ao mercado"
        }
      ]
    }
  ]
}
```

### chamados.json
```json
{
  "chamados": [
    {
      "id_cliente": "1",
      "historico_chamados": {
        "protocolo": "20250810023000PRT",
        "descricao": "Problema na conexão",
        "endereco_completo": [...],
        "data_abertura": "10-08-2025",
        "status": "aberto",
        "anotacoes": []
      }
    }
  ]
}
```

### cobertura.json
```json
{
  "cobertura": [
    {
      "endereco_cadastrado": "...",
      "cidade": "Britânia",
      "bairro": "Centro",
      "status": "coberto"
    }
  ]
}
```

## Testes

### Teste Manual via Interface Web

1. Acesse `http://localhost:5173`
2. Interaja com o chatbot seguindo os fluxos
3. Verifique as respostas e persistência de dados

### Teste via API

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "message": "ola"}'
```

## Integração com WhatsApp

O sistema está preparado para integração com a API WAHA (WhatsApp HTTP API). Para ativar:

1. Configure as credenciais da API WAHA
2. Atualize o endpoint `/webhook` conforme a documentação da WAHA
3. Configure os webhooks no painel da WAHA

## Integração com OpenAI

Para funcionalidades de IA avançadas:

1. Configure a variável de ambiente `OPENAI_API_KEY`
2. Implemente processamento de linguagem natural no backend
3. Adicione funcionalidades de aprendizado automático

## Monitoramento e Logs

O sistema gera logs automáticos para:

- Interações de usuários
- Criação de chamados
- Erros de sistema
- Métricas de performance

## Segurança

### Medidas Implementadas

- Validação de entrada de dados
- Sanitização de CPF
- CORS configurado para desenvolvimento
- Estrutura preparada para autenticação

### Recomendações para Produção

- Implementar HTTPS
- Configurar autenticação JWT
- Adicionar rate limiting
- Implementar logs de auditoria
- Configurar backup automático dos dados

## Deployment

### Desenvolvimento Local

Siga as instruções de instalação acima.

### Produção

1. **Backend**: Configure um servidor WSGI (Gunicorn, uWSGI)
2. **Frontend**: Build e deploy em servidor web (Nginx, Apache)
3. **Banco de Dados**: Migre para PostgreSQL ou MongoDB
4. **Monitoramento**: Configure logs e métricas

## Manutenção

### Backup dos Dados

```bash
# Backup diário dos arquivos JSON
cp data/*.json backup/$(date +%Y%m%d)/
```

### Atualizações

1. Teste em ambiente de desenvolvimento
2. Faça backup dos dados
3. Deploy gradual com rollback preparado

## Suporte

Para suporte técnico ou dúvidas sobre implementação:

- Documentação técnica: Consulte os comentários no código
- Logs de erro: Verifique os logs do Flask e do React
- Testes: Execute os testes automatizados antes de mudanças
