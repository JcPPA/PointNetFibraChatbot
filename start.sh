#!/bin/bash

# Script de inicialização do Chatbot Theo - Point Net Fibra

echo "=== Iniciando Chatbot Theo - Point Net Fibra ==="

# Função para parar processos ao sair
cleanup() {
    echo ""
    echo "Parando serviços..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "Serviços parados."
    exit
}

# Capturar Ctrl+C
trap cleanup SIGINT

# Verificar se os diretórios existem
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "Erro: Diretórios backend ou frontend não encontrados!"
    echo "Execute este script a partir do diretório raiz do projeto."
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d "backend/venv" ]; then
    echo "Erro: Ambiente virtual não encontrado!"
    echo "Execute primeiro: cd backend && python3.11 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Verificar se as dependências do frontend estão instaladas
if [ ! -d "frontend/node_modules" ]; then
    echo "Erro: Dependências do frontend não instaladas!"
    echo "Execute primeiro: cd frontend && pnpm install"
    exit 1
fi

echo "Iniciando backend..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!

# Aguardar backend inicializar
echo "Aguardando backend inicializar..."
sleep 5

# Verificar se o backend está rodando
if ! curl -s http://localhost:5000/health > /dev/null; then
    echo "Erro: Backend não conseguiu inicializar!"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "Backend iniciado com sucesso!"

# Iniciar frontend
echo "Iniciando frontend..."
cd ../frontend
pnpm run dev --host &
FRONTEND_PID=$!

# Aguardar frontend inicializar
echo "Aguardando frontend inicializar..."
sleep 5

echo ""
echo "=== Sistema iniciado com sucesso! ==="
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:5173"
echo "Health Check: http://localhost:5000/health"
echo ""
echo "Pressione Ctrl+C para parar todos os serviços"
echo ""

# Aguardar indefinidamente
wait

