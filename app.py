from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Permitir CORS para todas as rotas

# Caminhos para os arquivos JSON
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CLIENTES_FILE = os.path.join(DATA_DIR, 'clientes.json')
CHAMADOS_FILE = os.path.join(DATA_DIR, 'chamados.json')
COBERTURA_FILE = os.path.join(DATA_DIR, 'cobertura.json')

class ChatbotTheo:
    def __init__(self):
        self.user_sessions = {}  # Armazenar estado das sessões dos usuários
    
    def load_json_file(self, file_path):
        """Carrega dados de um arquivo JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
    
    def save_json_file(self, file_path, data):
        """Salva dados em um arquivo JSON"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_greeting_message(self):
        """Retorna a mensagem de saudação baseada no horário"""
        now = datetime.now()
        hour = now.hour
        
        if 6 <= hour <= 12:
            return "Olá, seja bem-vindo(a) a Point Net Fibra, em que posso ajudar?"
        elif 13 <= hour <= 18:
            return "Olá, seja bem-vindo(a) a Point Net Fibra, em que posso ser útil?"
        else:
            return "Olá, seja bem-vindo(a) a Point Net Fibra, em que posso auxiliar?"
    
    def get_classification_menu(self):
        """Retorna o menu de classificação de atendimento"""
        return """2) Classificação de Atendimento:
a1) Cliente novo (cadastro) ou Primeiro atendimento; ou
a2) Informações sobre planos (vendas), promoções e mudança de planos; ou
a3) Informações sobre pagamento ou débitos; ou
a4) Problemas técnicos (suporte). ou
a5) Cancelamento ou mudança de endereço.
[OBSERVAÇÃO: o cliente deverá responder apenas o termo do ítem, por exemplo, 'a.1' que quer dizer 'Cliente novo (cadastro) ou primeiro atendimento']."""
    
    def search_client_by_cpf(self, cpf):
        """Busca cliente por CPF"""
        clientes_data = self.load_json_file(CLIENTES_FILE)
        for cliente in clientes_data.get('clientes', []):
            if cliente.get('cpf') == cpf:
                return cliente
        return None
    
    def generate_new_client_id(self):
        """Gera um novo ID sequencial para cliente"""
        clientes_data = self.load_json_file(CLIENTES_FILE)
        clientes = clientes_data.get('clientes', [])
        if not clientes:
            return "1"
        
        max_id = max(int(cliente.get('id', '0')) for cliente in clientes)
        return str(max_id + 1)
    
    def save_new_client(self, client_data):
        """Salva um novo cliente"""
        clientes_data = self.load_json_file(CLIENTES_FILE)
        if 'clientes' not in clientes_data:
            clientes_data['clientes'] = []
        
        client_data['id'] = self.generate_new_client_id()
        clientes_data['clientes'].append(client_data)
        self.save_json_file(CLIENTES_FILE, clientes_data)
        return client_data['id']
    
    def generate_protocol(self):
        """Gera um protocolo único"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{timestamp}PRT"
    
    def create_chamado(self, client_id, description):
        """Cria um novo chamado"""
        chamados_data = self.load_json_file(CHAMADOS_FILE)
        if 'chamados' not in chamados_data:
            chamados_data['chamados'] = []
        
        # Buscar dados do cliente
        cliente = None
        clientes_data = self.load_json_file(CLIENTES_FILE)
        for c in clientes_data.get('clientes', []):
            if c.get('id') == client_id:
                cliente = c
                break
        
        if not cliente:
            return None
        
        protocol = self.generate_protocol()
        
        chamado = {
            "id_cliente": client_id,
            "historico_chamados": {
                "protocolo": protocol,
                "descricao": description,
                "endereco_completo": cliente.get('enderecos', []),
                "data_abertura": datetime.now().strftime("%d-%m-%Y"),
                "status": "aberto",
                "anotacoes": []
            }
        }
        
        chamados_data['chamados'].append(chamado)
        self.save_json_file(CHAMADOS_FILE, chamados_data)
        
        return {
            "protocolo": protocol,
            "cliente": cliente
        }
    
    def check_coverage(self, endereco):
        """Verifica cobertura de um endereço"""
        cobertura_data = self.load_json_file(COBERTURA_FILE)
        # Implementação simplificada - assumindo que cobertura.json tem uma lista de endereços cobertos
        enderecos_cobertos = cobertura_data.get('cobertura', [])
        
        # Aqui você pode implementar uma lógica mais sofisticada de verificação
        # Por enquanto, vamos assumir que qualquer endereço está coberto para teste
        return True
    
    def process_message(self, user_id, message):
        """Processa uma mensagem do usuário"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                'state': 'greeting',
                'data': {}
            }
        
        session = self.user_sessions[user_id]
        state = session['state']
        
        if state == 'greeting':
            greeting = self.get_greeting_message()
            classification = self.get_classification_menu()
            session['state'] = 'waiting_classification'
            return f"{greeting}\n\n{classification}"
        
        elif state == 'waiting_classification':
            message = message.lower().strip()
            if message in ['a1', 'a.1']:
                session['state'] = 'cadastro_cpf'
                session['data']['flow'] = 'cadastro'
                return "b1) Qual o nº de CPF do cliente (sem ponto e traço)?"
            elif message in ['a2', 'a.2']:
                session['state'] = 'planos_cpf'
                session['data']['flow'] = 'planos'
                return "c.1.1 - Qual o seu CPF?"
            elif message in ['a3', 'a.3']:
                session['state'] = 'pagamento'
                return "Para informações sobre pagamento ou débitos, você será direcionado para um atendente."
            elif message in ['a4', 'a.4']:
                session['state'] = 'cadastro_cpf'
                session['data']['flow'] = 'suporte'
                return "b1) Qual o nº de CPF do cliente (sem ponto e traço)?"
            elif message in ['a5', 'a.5']:
                session['state'] = 'encaminhar_atendente'
                return "Aguarde um momento por favor, estaremos direcionando seu atendimento para nossos atendentes."
            else:
                return "Por favor, responda com uma das opções: a1, a2, a3, a4 ou a5."
        
        elif state == 'cadastro_cpf':
            cpf = message.strip()
            cliente = self.search_client_by_cpf(cpf)
            
            if cliente:
                session['data']['cliente_encontrado'] = cliente
                session['state'] = 'confirmar_cliente'
                return f"""Este é você?
"nome_completo": "{cliente.get('nome_completo', '')}",
"telefone": "{cliente.get('telefone', '')}"."""
            else:
                session['data']['cpf'] = cpf
                session['state'] = 'cadastro_nome'
                return "b2) Qual o seu nome completo (sem acento)?"
        
        elif state == 'confirmar_cliente':
            resposta = message.lower().strip()
            if resposta in ['sim', 's', 'yes']:
                if session['data']['flow'] == 'suporte':
                    session['state'] = 'problema_descricao'
                    return "b9) Qual o problema/solicitação deseja realizar?"
                else:
                    session['state'] = 'problema_descricao'
                    return "b9) Qual o problema/solicitação deseja realizar?"
            elif resposta in ['não', 'nao', 'n', 'no']:
                session['state'] = 'cadastro_nome'
                return "b2) Qual o seu nome completo (sem acento)?"
            else:
                return "Por favor, responda com 'sim' ou 'não'."
        
        elif state == 'cadastro_nome':
            session['data']['nome_completo'] = message.strip()
            session['state'] = 'cadastro_telefone'
            return "b3) Qual o seu telefone para contato?"
        
        elif state == 'cadastro_telefone':
            session['data']['telefone'] = message.strip()
            session['state'] = 'cadastro_cep'
            return "b4) Qual a seu CEP?"
        
        elif state == 'cadastro_cep':
            session['data']['cep'] = message.strip()
            session['state'] = 'cadastro_logradouro'
            return "b5) Qual o seu Logradouro?"
        
        elif state == 'cadastro_logradouro':
            session['data']['logradouro'] = message.strip()
            session['state'] = 'cadastro_numero'
            return "b6) Qual o seu nº da sua residência?"
        
        elif state == 'cadastro_numero':
            session['data']['numero'] = message.strip()
            session['state'] = 'cadastro_bairro'
            return "b7) Qual o seu bairro?"
        
        elif state == 'cadastro_bairro':
            session['data']['bairro'] = message.strip()
            session['state'] = 'cadastro_complemento'
            return "b8) Existe um ponto de referência próximo a sua casa?"
        
        elif state == 'cadastro_complemento':
            session['data']['complemento'] = message.strip()
            
            # Salvar cliente
            client_data = {
                "cpf": session['data']['cpf'],
                "nome_completo": session['data']['nome_completo'],
                "telefone": session['data']['telefone'],
                "enderecos": [{
                    "cep": session['data']['cep'],
                    "estado": "GO",  # Assumindo Goiás baseado nas cidades mencionadas
                    "cidade": "Britânia",  # Assumindo baseado no contexto
                    "logradouro": session['data']['logradouro'],
                    "numero": session['data']['numero'],
                    "bairro": session['data']['bairro'],
                    "complemento": session['data']['complemento']
                }]
            }
            
            client_id = self.save_new_client(client_data)
            session['data']['client_id'] = client_id
            session['state'] = 'problema_descricao'
            return "b9) Qual o problema/solicitação deseja realizar?"
        
        elif state == 'problema_descricao':
            description = message.strip()
            
            # Determinar client_id
            if 'cliente_encontrado' in session['data']:
                client_id = session['data']['cliente_encontrado']['id']
                cliente = session['data']['cliente_encontrado']
            else:
                client_id = session['data']['client_id']
                # Buscar cliente recém-criado
                clientes_data = self.load_json_file(CLIENTES_FILE)
                cliente = None
                for c in clientes_data.get('clientes', []):
                    if c.get('id') == client_id:
                        cliente = c
                        break
            
            # Criar chamado
            chamado_info = self.create_chamado(client_id, description)
            
            if chamado_info:
                endereco_completo = ""
                if cliente and 'enderecos' in cliente and cliente['enderecos']:
                    endereco = cliente['enderecos'][0]
                    endereco_completo = f"{endereco.get('logradouro', '')} {endereco.get('numero', '')} {endereco.get('bairro', '')} {endereco.get('complemento', '')}"
                
                # Simular notificação para o servidor (WhatsApp)
                notification = f"""Chamado em Aberto!
Protocolo: {chamado_info['protocolo']}
Cliente: {cliente.get('nome_completo', '')}
Contato: {cliente.get('telefone', '')}
UF: GO
Endereço: {endereco_completo}"""
                
                # Reset da sessão
                session['state'] = 'greeting'
                session['data'] = {}
                
                return "Chamado cadastrado com sucesso! Aguarde contato de nosso suporte ou de nosso atendente."
            else:
                return "Erro ao criar chamado. Tente novamente."
        
        elif state == 'planos_cpf':
            cpf = message.strip()
            cliente = self.search_client_by_cpf(cpf)
            
            if cliente:
                # Verificar cobertura
                if cliente.get('enderecos'):
                    endereco = cliente['enderecos'][0]
                    if self.check_coverage(endereco):
                        session['state'] = 'mostrar_planos'
                        return """c.2 - Nossos Planos:
c.2.1 - Britânia/Cidade (planos abaixo [valor e plano]); ou
c.2.2 - Britânia/Fazendas (planos abaixo [valor e plano]); ou
c.2.3 - Britânia/Itacaiu (planos abaixo [valor e plano]); ou
c.2.4 - Aruanã (planos abaixo [valor e plano]); ou
c.3 - Mais informações com o Atendente humano."""
                    else:
                        session['state'] = 'area_nao_coberta'
                        return """II) Área não coberta.
1 - Gostaria de retornar ao menu inicial? ou
2 - Gostaria de falar com um de nossos atendentes?"""
                else:
                    return "Cliente encontrado, mas sem endereço cadastrado. Por favor, entre em contato com nosso atendimento."
            else:
                session['state'] = 'planos_cep'
                return "c.1.2 - Qual o seu CEP?"
        
        elif state == 'planos_cep':
            cep = message.strip()
            # Verificar cobertura por CEP (implementação simplificada)
            if self.check_coverage({'cep': cep}):
                session['state'] = 'mostrar_planos'
                return """I) Área coberta.
c.2 - Nossos Planos:
c.2.1 - Britânia/Cidade (planos abaixo [valor e plano]); ou
c.2.2 - Britânia/Fazendas (planos abaixo [valor e plano]); ou
c.2.3 - Britânia/Itacaiu (planos abaixo [valor e plano]); ou
c.2.4 - Aruanã (planos abaixo [valor e plano]); ou
c.3 - Mais informações com o Atendente humano."""
            else:
                session['state'] = 'area_nao_coberta'
                return """II) Área não coberta.
1 - Gostaria de retornar ao menu inicial? ou
2 - Gostaria de falar com um de nossos atendentes?"""
        
        elif state == 'mostrar_planos':
            if message.strip().lower() == 'c.3':
                session['state'] = 'encaminhar_atendente'
                return "Aguarde um momento por favor, estaremos direcionando seu atendimento para nossos atendentes."
            else:
                return "Por favor, selecione uma das opções de planos ou digite 'c.3' para falar com um atendente."
        
        elif state == 'area_nao_coberta':
            resposta = message.strip()
            if resposta == '1':
                session['state'] = 'greeting'
                session['data'] = {}
                return "Obrigado pelo contato, volte sempre!"
            elif resposta == '2':
                session['state'] = 'encaminhar_atendente'
                return "Aguarde um momento por favor, estaremos direcionando seu atendimento para nossos atendentes."
            else:
                return "Por favor, responda com '1' ou '2'."
        
        else:
            session['state'] = 'greeting'
            session['data'] = {}
            return "Sessão reiniciada. " + self.get_greeting_message()

# Instância global do chatbot
chatbot = ChatbotTheo()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint para receber mensagens do WhatsApp"""
    try:
        data = request.get_json()
        
        # Extrair informações da mensagem (formato pode variar dependendo da API do WhatsApp)
        user_id = data.get('from', 'unknown')
        message = data.get('text', '')
        
        # Processar mensagem
        response = chatbot.process_message(user_id, message)
        
        return jsonify({
            'status': 'success',
            'response': response
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint para teste do chatbot via API"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'test_user')
        message = data.get('message', '')
        
        response = chatbot.process_message(user_id, message)
        
        return jsonify({
            'status': 'success',
            'response': response
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de saúde"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

