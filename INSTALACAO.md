# Guia de Instalação - Chatbot Theo Point Net Fibra

## Passo a Passo Completo de Instalação

Este guia fornece instruções detalhadas para configurar e executar o Chatbot Theo em diferentes ambientes.

## Pré-requisitos do Sistema

### Requisitos Mínimos

- **Sistema Operacional**: Linux (Ubuntu 20.04+), macOS (10.15+), ou Windows 10+
- **Memória RAM**: 4GB mínimo, 8GB recomendado
- **Espaço em Disco**: 2GB livres
- **Conexão com Internet**: Necessária para instalação de dependências

### Software Necessário

1. **Python 3.11 ou superior**
   ```bash
   # Verificar versão instalada
   python3 --version
   
   # Ubuntu/Debian - Instalar Python 3.11
   sudo apt update
   sudo apt install python3.11 python3.11-venv python3.11-pip
   
   # macOS - Usando Homebrew
   brew install python@3.11
   
   # Windows - Baixar do site oficial
   # https://www.python.org/downloads/
   ```

2. **Node.js 20.x ou superior**
   ```bash
   # Verificar versão instalada
   node --version
   
   # Ubuntu/Debian - Usando NodeSource
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt-get install -y nodejs
   
   # macOS - Usando Homebrew
   brew install node@20
   
   # Windows - Baixar do site oficial
   # https://nodejs.org/
   ```

3. **pnpm (Gerenciador de Pacotes)**
   ```bash
   # Instalar pnpm globalmente
   npm install -g pnpm
   
   # Verificar instalação
   pnpm --version
   ```

## Instalação Passo a Passo

### Etapa 1: Obter o Código

```bash
# Se usando Git
git clone <repositorio-do-projeto>
cd chatbot_pointnet

# Ou extrair de arquivo ZIP
unzip chatbot_pointnet.zip
cd chatbot_pointnet
```

### Etapa 2: Configurar o Backend

#### 2.1 Navegar para o Diretório do Backend
```bash
cd backend
```

#### 2.2 Criar Ambiente Virtual
```bash
# Linux/macOS
python3.11 -m venv venv

# Windows
python -m venv venv
```

#### 2.3 Ativar Ambiente Virtual
```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Você deve ver `(venv)` no início do prompt, indicando que o ambiente virtual está ativo.

#### 2.4 Instalar Dependências Python
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2.5 Verificar Instalação do Backend
```bash
python app.py
```

Se tudo estiver correto, você verá:
```
* Serving Flask app 'app'
* Debug mode: on
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
```

Pressione `Ctrl+C` para parar o servidor.

### Etapa 3: Configurar o Frontend

#### 3.1 Abrir Novo Terminal
Mantenha o terminal do backend aberto e abra um novo terminal.

#### 3.2 Navegar para o Diretório do Frontend
```bash
cd chatbot_pointnet/frontend
```

#### 3.3 Instalar Dependências Node.js
```bash
pnpm install
```

#### 3.4 Verificar Instalação do Frontend
```bash
pnpm run dev --host
```

Se tudo estiver correto, você verá:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.x.x:5173/
```

### Etapa 4: Configurar Dados Iniciais

#### 4.1 Verificar Arquivos de Dados
```bash
# Voltar ao diretório raiz
cd ..

# Verificar se os arquivos existem
ls -la data/
```

Você deve ver:
- `clientes.json`
- `chamados.json`
- `cobertura.json`

#### 4.2 Configurar Dados de Cobertura (Opcional)
Edite o arquivo `data/cobertura.json` para adicionar áreas cobertas:

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
    }
  ]
}
```

## Executando o Sistema

### Método 1: Execução Manual

#### Terminal 1 - Backend
```bash
cd chatbot_pointnet/backend
source venv/bin/activate  # Linux/macOS
# ou venv\Scripts\activate  # Windows
python app.py
```

#### Terminal 2 - Frontend
```bash
cd chatbot_pointnet/frontend
pnpm run dev --host
```

### Método 2: Script de Inicialização (Linux/macOS)

Crie um script `start.sh`:

```bash
#!/bin/bash

# Função para parar processos ao sair
cleanup() {
    echo "Parando serviços..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Capturar Ctrl+C
trap cleanup SIGINT

# Iniciar backend
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!

# Aguardar backend inicializar
sleep 3

# Iniciar frontend
cd ../frontend
pnpm run dev --host &
FRONTEND_PID=$!

echo "Sistema iniciado!"
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:5173"
echo "Pressione Ctrl+C para parar"

# Aguardar
wait
```

Tornar executável e executar:
```bash
chmod +x start.sh
./start.sh
```

## Testando a Instalação

### Teste 1: Verificar Backend
```bash
curl http://localhost:5000/health
```

Resposta esperada:
```json
{"status": "healthy"}
```

### Teste 2: Verificar API do Chatbot
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "message": "ola"}'
```

### Teste 3: Verificar Frontend
1. Abra o navegador
2. Acesse `http://localhost:5173`
3. Você deve ver a interface do Chatbot Theo
4. Digite uma mensagem e verifique se recebe resposta

## Solução de Problemas

### Problema: "Python não encontrado"
**Solução**:
```bash
# Ubuntu/Debian
sudo apt install python3.11

# Verificar instalação
python3.11 --version
```

### Problema: "pip não encontrado"
**Solução**:
```bash
# Ubuntu/Debian
sudo apt install python3.11-pip

# macOS
python3.11 -m ensurepip --upgrade
```

### Problema: "Node.js não encontrado"
**Solução**:
```bash
# Instalar Node.js via NodeSource (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Problema: "pnpm não encontrado"
**Solução**:
```bash
npm install -g pnpm
```

### Problema: "Porta 5000 em uso"
**Solução**:
```bash
# Encontrar processo usando a porta
lsof -i :5000

# Parar processo (substitua PID)
kill -9 <PID>

# Ou usar porta diferente
export FLASK_RUN_PORT=5001
```

### Problema: "Porta 5173 em uso"
**Solução**:
```bash
# Usar porta diferente
pnpm run dev --host --port 3000
```

### Problema: "Erro de CORS"
**Verificação**:
1. Certifique-se de que o backend está rodando
2. Verifique se Flask-CORS está instalado
3. Confirme que o frontend está acessando a URL correta

### Problema: "Arquivos JSON não encontrados"
**Solução**:
```bash
# Criar arquivos se não existirem
mkdir -p data
echo '{"clientes": []}' > data/clientes.json
echo '{"chamados": []}' > data/chamados.json
echo '{"cobertura": []}' > data/cobertura.json
```

## Configuração para Produção

### Backend - Usando Gunicorn
```bash
# Instalar Gunicorn
pip install gunicorn

# Executar em produção
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend - Build para Produção
```bash
cd frontend
pnpm run build

# Servir arquivos estáticos
npx serve dist -p 3000
```

### Usando Docker (Opcional)

#### Dockerfile para Backend
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
COPY data/ ../data/

EXPOSE 5000
CMD ["python", "app.py"]
```

#### Dockerfile para Frontend
```dockerfile
FROM node:20-alpine

WORKDIR /app
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

COPY frontend/ .
RUN pnpm run build

FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
EXPOSE 80
```

## Manutenção

### Backup Regular
```bash
# Script de backup
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p backups/$DATE
cp -r data/ backups/$DATE/
echo "Backup criado em backups/$DATE"
```

### Atualização de Dependências
```bash
# Backend
cd backend
source venv/bin/activate
pip list --outdated
pip install --upgrade <pacote>

# Frontend
cd frontend
pnpm outdated
pnpm update
```

### Logs e Monitoramento
```bash
# Ver logs do Flask
tail -f backend/app.log

# Monitorar processos
ps aux | grep -E "(python|node)"
```

## Suporte

Para problemas não cobertos neste guia:

1. Verifique os logs de erro
2. Confirme que todas as dependências estão instaladas
3. Teste cada componente individualmente
4. Consulte a documentação das tecnologias utilizadas

---

**Última atualização**: Agosto 2025  
**Versão do Guia**: 1.0.0

