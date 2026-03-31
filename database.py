# --- CRIAÇÃO E CONFIGURAÇÃO DO BANCO DE DADOS SQLite --- 

import sqlite3

# Constante com o nome do arquivo de banco de dados
# O arquivo será criado durante a primeira execução
bd_ordem = 'ordens.bd'

def get_connection():
    '''
    |Cria e retorna uma conexão com o banco de dados SQLite
    
    |A propriedade row_factory permite acessar as colunas pelo nome 
    |(Ex: Ordem ['produto'] em vez de pelo índice (Ex: Ordem[1]))
    
    |Retorna:
        sqlite3.Connection: objeto de conexão com o banco de dados.
    '''
    
    conn = sqlite3.connect(bd_ordem)
    conn.row_factory = sqlite3.Row
    return conn

def init_bd():
    '''
    |Inicializa o banco de dados criando a tabela 'ordens' se ela ainda não existir.
    |Seguro para chamar múltiplas vezes.
    '''
    conn = get_connection()
    
    # Cursor() permitir executar comandos SQL
    cursor = conn.cursor()
    
    # IF NOT EXIST - vai garantir que o comando não falhe se a tabela já existir
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS ordens(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       produto      TEXT      NOT NULL,
                       quantidade   INTEGER   NOT NULL,
                       status       TEXT      DEFAULT 'Pendente',
                       criado_em    TEXT      DEFAULT(datetime('now', 'localtime'))
                       )
                       ''')
    #commit() - vai salvar as alteraçoes no aquivo .bd
    conn.commit()
    
    #close() - liberar a conexão (Boa Prática)
    conn.close()
    
    print("Banco de dados iniciado com sucesso!")
    