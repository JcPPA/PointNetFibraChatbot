# Configuração Docker - Chatbot Theo Point Net Fibra

## Visão Geral

Este documento fornece instruções para executar o Chatbot Theo usando Docker e Docker Compose, facilitando o deployment e a manutenção do sistema.

## Pré-requisitos

- Docker 20.10 ou superior
- Docker Compose 2.0 ou superior

### Instalação do Docker

#### Ubuntu/Debian
```bash
# Remover versões antigas
sudo apt-get remove docker docker-engine docker.io containerd runc

# Instalar dependências
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release

# Adicionar chave GPG oficial do Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Configurar repositório
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
```

#### macOS
```bash
# Usando Homebrew
brew install --cask docker

# Ou baixar Docker Desktop do site oficial
# https://www.docker.com/products/docker-desktop
```

#### Windows
Baixe e instale o Docker Desktop do site oficial: https://www.docker.com/products/docker-desktop

## Arquivos Docker

### Dockerfile - Backend

Crie o arquivo `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para dados
RUN mkdir -p /app/data

# Expor porta
EXPOSE 5000

# Definir variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Comando para executar a aplicação
CMD ["python", "app.py"]
```

### Dockerfile - Frontend

Crie o arquivo `frontend/Dockerfile`:

```dockerfile
# Estágio de build
FROM node:20-alpine AS builder

WORKDIR /app

# Copiar arquivos de dependências
COPY package.json pnpm-lock.yaml ./

# Instalar pnpm e dependências
RUN npm install -g pnpm
RUN pnpm install --frozen-lockfile

# Copiar código fonte
COPY . .

# Build da aplicação
RUN pnpm run build

# Estágio de produção
FROM nginx:alpine

# Copiar arquivos buildados
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuração customizada do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expor porta
EXPOSE 80

# Comando padrão do Nginx
CMD ["nginx", "-g", "daemon off;"]
```

### Configuração do Nginx

Crie o arquivo `frontend/nginx.conf`:

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Configuração para SPA (Single Page Application)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Configuração para arquivos estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy para API do backend
    location /api/ {
        proxy_pass http://backend:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Configurações de segurança
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}
```

### Docker Compose

Crie o arquivo `docker-compose.yml` na raiz do projeto:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: chatbot-backend
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - backend_logs:/app/logs
    environment:
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
    networks:
      - chatbot-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: chatbot-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - chatbot-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  backend_logs:

networks:
  chatbot-network:
    driver: bridge
```

### Docker Compose para Desenvolvimento

Crie o arquivo `docker-compose.dev.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: chatbot-backend-dev
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app
      - ./data:/app/data
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
      - PYTHONUNBUFFERED=1
    networks:
      - chatbot-network
    command: python app.py

  frontend:
    image: node:20-alpine
    container_name: chatbot-frontend-dev
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
    working_dir: /app
    environment:
      - NODE_ENV=development
    networks:
      - chatbot-network
    command: sh -c "npm install -g pnpm && pnpm install && pnpm run dev --host"

networks:
  chatbot-network:
    driver: bridge
```

## Comandos Docker

### Build e Execução

#### Produção
```bash
# Build das imagens
docker-compose build

# Executar em background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down
```

#### Desenvolvimento
```bash
# Executar em modo desenvolvimento
docker-compose -f docker-compose.dev.yml up

# Executar em background
docker-compose -f docker-compose.dev.yml up -d

# Rebuild e restart
docker-compose -f docker-compose.dev.yml up --build
```

### Comandos Úteis

```bash
# Ver status dos containers
docker-compose ps

# Executar comando no container
docker-compose exec backend bash
docker-compose exec frontend sh

# Ver logs de um serviço específico
docker-compose logs backend
docker-compose logs frontend

# Restart de um serviço
docker-compose restart backend

# Remover tudo (containers, volumes, networks)
docker-compose down -v --remove-orphans
```

## Configuração de Produção

### Variáveis de Ambiente

Crie o arquivo `.env`:

```env
# Configurações do Flask
FLASK_ENV=production
FLASK_SECRET_KEY=sua-chave-secreta-muito-segura

# Configurações do banco de dados (se usar PostgreSQL)
DATABASE_URL=postgresql://user:password@db:5432/chatbot

# Configurações de API externa
WHATSAPP_API_URL=https://api.whatsapp.com
WHATSAPP_API_TOKEN=seu-token-aqui

OPENAI_API_KEY=sua-chave-openai-aqui

# Configurações de email (se necessário)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-app
```

### Docker Compose com PostgreSQL

Para usar PostgreSQL em vez de arquivos JSON:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: chatbot-db
    environment:
      POSTGRES_DB: chatbot
      POSTGRES_USER: chatbot_user
      POSTGRES_PASSWORD: senha_segura
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - chatbot-network
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: chatbot-backend
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://chatbot_user:senha_segura@db:5432/chatbot
    depends_on:
      - db
    networks:
      - chatbot-network
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: chatbot-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - chatbot-network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  chatbot-network:
    driver: bridge
```

## Monitoramento e Logs

### Configuração de Logs

Adicione ao `docker-compose.yml`:

```yaml
services:
  backend:
    # ... outras configurações
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  frontend:
    # ... outras configurações
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Scripts de Monitoramento

Crie o arquivo `scripts/monitor.sh`:

```bash
#!/bin/bash

echo "=== Status dos Containers ==="
docker-compose ps

echo -e "\n=== Uso de Recursos ==="
docker stats --no-stream

echo -e "\n=== Logs Recentes do Backend ==="
docker-compose logs --tail=10 backend

echo -e "\n=== Logs Recentes do Frontend ==="
docker-compose logs --tail=10 frontend

echo -e "\n=== Health Checks ==="
curl -s http://localhost:5000/health | jq .
curl -s -o /dev/null -w "%{http_code}" http://localhost/
```

## Backup e Restore

### Script de Backup

Crie o arquivo `scripts/backup.sh`:

```bash
#!/bin/bash

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/$DATE"

mkdir -p $BACKUP_DIR

# Backup dos dados
docker-compose exec -T backend tar czf - /app/data | cat > $BACKUP_DIR/data.tar.gz

# Backup do banco (se usar PostgreSQL)
docker-compose exec -T db pg_dump -U chatbot_user chatbot | gzip > $BACKUP_DIR/database.sql.gz

# Backup dos volumes
docker run --rm -v chatbot_backend_logs:/data -v $(pwd)/$BACKUP_DIR:/backup alpine tar czf /backup/logs.tar.gz -C /data .

echo "Backup criado em $BACKUP_DIR"
```

### Script de Restore

Crie o arquivo `scripts/restore.sh`:

```bash
#!/bin/bash

if [ -z "$1" ]; then
    echo "Uso: $0 <diretorio_backup>"
    exit 1
fi

BACKUP_DIR=$1

# Parar serviços
docker-compose down

# Restore dos dados
cat $BACKUP_DIR/data.tar.gz | docker run --rm -i -v $(pwd)/data:/data alpine tar xzf - -C /

# Restore do banco (se usar PostgreSQL)
zcat $BACKUP_DIR/database.sql.gz | docker-compose exec -T db psql -U chatbot_user chatbot

# Restart dos serviços
docker-compose up -d

echo "Restore concluído de $BACKUP_DIR"
```

## Deployment em Produção

### Usando Docker Swarm

```bash
# Inicializar swarm
docker swarm init

# Deploy do stack
docker stack deploy -c docker-compose.yml chatbot

# Ver serviços
docker service ls

# Escalar serviços
docker service scale chatbot_backend=3
```

### Usando Kubernetes

Crie os arquivos de deployment em `k8s/`:

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: chatbot

---
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chatbot-backend
  namespace: chatbot
spec:
  replicas: 3
  selector:
    matchLabels:
      app: chatbot-backend
  template:
    metadata:
      labels:
        app: chatbot-backend
    spec:
      containers:
      - name: backend
        image: chatbot-backend:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
```

## Troubleshooting

### Problemas Comuns

#### Container não inicia
```bash
# Ver logs detalhados
docker-compose logs backend

# Verificar configuração
docker-compose config

# Rebuild da imagem
docker-compose build --no-cache backend
```

#### Problemas de rede
```bash
# Verificar redes
docker network ls

# Inspecionar rede
docker network inspect chatbot_chatbot-network

# Testar conectividade
docker-compose exec backend ping frontend
```

#### Problemas de volume
```bash
# Verificar volumes
docker volume ls

# Inspecionar volume
docker volume inspect chatbot_backend_logs

# Limpar volumes órfãos
docker volume prune
```

## Segurança

### Boas Práticas

1. **Não usar root nos containers**
2. **Usar imagens oficiais e atualizadas**
3. **Configurar secrets adequadamente**
4. **Limitar recursos dos containers**
5. **Usar networks isoladas**

### Exemplo de configuração segura

```yaml
services:
  backend:
    # ... outras configurações
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
```

---

**Última atualização**: Agosto 2025  
**Versão**: 1.0.0

