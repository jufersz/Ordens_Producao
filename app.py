#--- BACK-END FLASK: ROTAS DA API REST ---

from flask import Flask, jsonify, request
from flask_cors import CORS
from database import init_bd, get_connection

# Cria uma instância da aplicação Flash
app = Flask(__name__, static_folder = 'static', static_url_path='')

# Habilitar os CORS
CORS(app)

# ROTA Nº1 - PÁGINA INICIAL
@app.route('/')
def index():
    # Alimentar o arquivo INDEX.HTML da pasta STATIC
    return app.send_static_file('index.html')

# ROTA Nº2 - STATUS API
@app.route('/status')
def status():
    # Rota de verificação da API(saúde)
    # Retora um JSON informando que o servidor está vivo
    return jsonify({
        "status": "online",
        "sistema": "Sistema de ordem de Producao",
        "versao": "1.0.0",
        "mensagem": "Ola, Fabrica, API FUNCIONANDO!"
    })
# ROTA Nº3 - LISTAR TODAS AS ORDENS(GET)
@app.route('/ordens', methods=['GET'])
def listar_ordens():
    '''
    | Listar todas as ordens de produção cadastradas.
    | Métodos HTTP: GET
    | URL: http://localhost:5000/ordens
    | Retorna: Lista e ordens em formato JSON.
    '''
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ordens ORDER BY id DESC')
    ordens = cursor.fetchall()
    conn.close()
    
    # Converte cada Row do SQLite em um dicionário Python para serializar um JSON
    return jsonify([dict(o) for o in ordens])

# --- ROTA POR ID - BUSCAR UMA ORDEM ESPECÍFICA PELO ID (GET) ---

@app.route('/ordens/<int:ordem_id>', methods=['GET'])

def buscar_ordem(ordem_id):
    """
    Buscar uma única ordem de produção pelo ID.
    
    Parametros de URL:
        - Ordem id(int): ID da ordem a ser buscada
    
    Retornar:
        200 + JSON da ordem, se for encontrada.
        404 + mensagem de erro, se não existir
    """
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # O'?' é substituido pelo valor de ordem_id de forma segura
    cursor.execute('SELECT * FROM ordens WHERE id = ?', (ordem_id,))
    ordem = cursor.fetchone()  #ele retorna um unico registro ou None
    conn.close()
    
    
    if ordem is None:
        return jsonify({'erro': f'Ordem {ordem_id} nao encontrada'}), 404
    return jsonify(dict(ordem)), 200

# --- PONTO DE PARTIDA ---

if __name__=='__main__':
    init_bd()

    app.run(debug=True, host='0.0.0.0', port=5000)