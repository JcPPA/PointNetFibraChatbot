# Estrutura do Projeto - Chatbot Theo Point Net Fibra

## Visão Geral da Estrutura

Este documento detalha a organização completa dos arquivos e diretórios do projeto Chatbot Theo.

```
chatbot_pointnet/
├── README.md                    # Documentação principal do projeto
├── INSTALACAO.md               # Guia detalhado de instalação
├── DOCKER.md                   # Documentação para Docker
├── ESTRUTURA_PROJETO.md        # Este arquivo - estrutura do projeto
├── docker-compose.yml          # Configuração Docker Compose
├── start.sh                    # Script de inicialização rápida
├── todo.md                     # Lista de tarefas do projeto
│
├── backend/                    # Aplicação Flask (Python)
│   ├── app.py                  # Arquivo principal do servidor Flask
│   ├── requirements.txt        # Dependências Python
│   ├── Dockerfile             # Configuração Docker para backend
│   └── venv/                  # Ambiente virtual Python (criado na instalação)
│       ├── bin/
│       ├── lib/
│       └── ...
│
├── frontend/                   # Aplicação React
│   ├── src/                   # Código fonte React
│   │   ├── App.jsx            # Componente principal da aplicação
│   │   ├── App.css            # Estilos da aplicação
│   │   ├── main.jsx           # Ponto de entrada da aplicação
│   │   ├── index.css          # Estilos globais
│   │   ├── assets/            # Recursos estáticos
│   │   ├── components/        # Componentes React reutilizáveis
│   │   │   └── ui/            # Componentes UI (shadcn/ui)
│   │   ├── hooks/             # Custom React hooks
│   │   └── lib/               # Utilitários e bibliotecas
│   ├── public/                # Arquivos públicos
│   ├── index.html             # Template HTML principal
│   ├── package.json           # Dependências e scripts Node.js
│   ├── pnpm-lock.yaml         # Lock file das dependências
│   ├── vite.config.js         # Configuração do Vite
│   ├── tailwind.config.js     # Configuração do Tailwind CSS
│   ├── components.json        # Configuração shadcn/ui
│   ├── eslint.config.js       # Configuração ESLint
│   ├── Dockerfile             # Configuração Docker para frontend
│   ├── nginx.conf             # Configuração Nginx para produção
│   └── node_modules/          # Dependências instaladas (criado na instalação)
│
└── data/                      # Base de dados JSON
    ├── clientes.json          # Dados dos clientes
    ├── chamados.json          # Dados dos chamados/protocolos
    └── cobertura.json         # Dados de cobertura de serviços
```

## Detalhamento dos Arquivos

### Arquivos de Configuração Raiz

#### README.md
- **Propósito**: Documentação principal do projeto
- **Conteúdo**: Visão geral, instalação, uso, APIs, estrutura de dados
- **Público-alvo**: Desenvolvedores e administradores

#### INSTALACAO.md
- **Propósito**: Guia passo a passo de instalação
- **Conteúdo**: Pré-requisitos, instalação detalhada, solução de problemas
- **Público-alvo**: Técnicos responsáveis pela implantação

#### DOCKER.md
- **Propósito**: Documentação para containerização
- **Conteúdo**: Dockerfiles, Docker Compose, deployment, monitoramento
- **Público-alvo**: DevOps e administradores de sistema

#### docker-compose.yml
- **Propósito**: Orquestração de containers
- **Conteúdo**: Definição de serviços, redes, volumes
- **Uso**: `docker-compose up` para executar o sistema completo

#### start.sh
- **Propósito**: Script de inicialização rápida
- **Conteúdo**: Automação da inicialização de backend e frontend
- **Uso**: `./start.sh` para iniciar o sistema em desenvolvimento

### Backend (Flask/Python)

#### app.py
```python
# Estrutura principal:
- Classe ChatbotTheo: Lógica principal do chatbot
- Rotas Flask: /chat, /webhook, /health
- Gerenciamento de sessões de usuário
- Manipulação de arquivos JSON
- Lógica de fluxos de atendimento
```

**Principais funcionalidades**:
- Processamento de mensagens
- Gerenciamento de estado de conversação
- CRUD de clientes e chamados
- Validação de cobertura
- Geração de protocolos

#### requirements.txt
```
Flask==3.1.1
Flask-CORS==6.0.1
requests==2.31.0
```

#### Dockerfile
- **Base**: python:3.11-slim
- **Porta**: 5000
- **Volumes**: /app/data para persistência
- **Comando**: python app.py

### Frontend (React/Vite)

#### src/App.jsx
```javascript
// Componente principal com:
- Estado de mensagens
- Comunicação com API backend
- Interface de chat responsiva
- Gerenciamento de sessões de usuário
```

**Principais funcionalidades**:
- Interface de chat em tempo real
- Formatação de mensagens
- Indicadores de carregamento
- Responsividade mobile/desktop

#### src/App.css
- **Framework**: Tailwind CSS
- **Componentes**: shadcn/ui
- **Tema**: Configuração de cores e espaçamentos
- **Responsividade**: Breakpoints para diferentes telas

#### package.json
```json
{
  "dependencies": {
    "react": "^18.x",
    "vite": "^5.x",
    "tailwindcss": "^3.x",
    "@radix-ui/react-*": "componentes UI",
    "lucide-react": "ícones"
  }
}
```

#### vite.config.js
- **Bundler**: Vite para desenvolvimento rápido
- **Plugins**: React, Tailwind CSS
- **Proxy**: Configuração para API backend

### Base de Dados (JSON)

#### clientes.json
```json
{
  "clientes": [
    {
      "id": "string",
      "cpf": "string",
      "nome_completo": "string",
      "telefone": "string",
      "enderecos": [
        {
          "cep": "string",
          "estado": "string",
          "cidade": "string",
          "logradouro": "string",
          "numero": "string",
          "bairro": "string",
          "complemento": "string"
        }
      ]
    }
  ]
}
```

#### chamados.json
```json
{
  "chamados": [
    {
      "id_cliente": "string",
      "historico_chamados": {
        "protocolo": "string",
        "descricao": "string",
        "endereco_completo": "array",
        "data_abertura": "string",
        "status": "string",
        "anotacoes": []
      }
    }
  ]
}
```

#### cobertura.json
```json
{
  "cobertura": [
    {
      "endereco_cadastrado": "string",
      "cidade": "string",
      "bairro": "string",
      "cep": "string",
      "status": "string"
    }
  ]
}
```

## Fluxo de Dados

### 1. Interação do Usuário
```
Frontend (React) → API Request → Backend (Flask) → JSON Files
                ←              ←                 ←
```

### 2. Processamento de Mensagem
```
1. Usuário digita mensagem
2. Frontend envia POST /chat
3. Backend processa via ChatbotTheo.process_message()
4. Backend consulta/atualiza arquivos JSON
5. Backend retorna resposta
6. Frontend exibe resposta
```

### 3. Gerenciamento de Estado
```
- Sessões de usuário: Memória (user_sessions dict)
- Dados persistentes: Arquivos JSON
- Estado da UI: React state hooks
```

## Padrões de Código

### Backend (Python)
- **Estilo**: PEP 8
- **Estrutura**: Classes para organização
- **Error Handling**: Try/catch com logs
- **JSON**: Manipulação segura com validação

### Frontend (React)
- **Estilo**: ES6+ com JSX
- **Hooks**: useState, useEffect, useRef
- **Componentes**: Funcionais com props
- **Styling**: Tailwind CSS classes

## Configurações de Desenvolvimento

### Backend
```bash
# Ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Dependências
pip install -r requirements.txt

# Execução
python app.py
```

### Frontend
```bash
# Dependências
pnpm install

# Desenvolvimento
pnpm run dev --host

# Build produção
pnpm run build
```

## Configurações de Produção

### Docker
```bash
# Build e execução
docker-compose up -d

# Logs
docker-compose logs -f

# Parar
docker-compose down
```

### Nginx (Frontend)
- **Proxy**: /api/ → backend:5000
- **SPA**: Fallback para index.html
- **Cache**: Arquivos estáticos com cache longo
- **Segurança**: Headers de segurança configurados

## Monitoramento

### Health Checks
- **Backend**: GET /health
- **Frontend**: HTTP 200 na raiz
- **Docker**: Health checks automáticos

### Logs
- **Backend**: Console logs do Flask
- **Frontend**: Browser console
- **Docker**: docker-compose logs

## Backup e Manutenção

### Arquivos Críticos
- `data/*.json`: Dados dos clientes e chamados
- `backend/app.py`: Lógica principal
- `frontend/src/App.jsx`: Interface principal

### Backup Recomendado
```bash
# Diário
tar -czf backup_$(date +%Y%m%d).tar.gz data/

# Semanal
tar -czf backup_full_$(date +%Y%m%d).tar.gz .
```

## Extensibilidade

### Adição de Novos Fluxos
1. Modificar `ChatbotTheo.process_message()`
2. Adicionar novos estados na máquina de estados
3. Atualizar frontend se necessário

### Integração com APIs Externas
1. Adicionar configurações em variáveis de ambiente
2. Implementar clientes HTTP no backend
3. Adicionar tratamento de erros

### Migração para Banco de Dados
1. Substituir manipulação de JSON por ORM
2. Adicionar migrations
3. Configurar conexão de banco

---

**Última atualização**: Agosto 2025  
**Versão**: 1.0.0

