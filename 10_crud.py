# Importando biblioteca sqlite3
import sqlite3

# Conectar ao banco de dados (ou criar um novo se não existir)
def conectarBanco() :
    conexao = sqlite3.connect('exemplo.db')
    return conexao

# Vamos criar uma tabela
def criarTabela() :
    conexao = conectarBanco()
    cursor = conexao.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS usuarios (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT,
                       idade INTEGER
                   )
                   ''')
    conexao.commit()
    conexao.close()

# Inserir usuario    
def inserirUsuario(nome, idade) :
    conexao = conectarBanco()
    cursor = conexao.cursor()
    cursor.execute('''
                   INSERT INTO usuarios (nome, idade) VALUES (?, ?)
                   ''', (nome, idade))
    conexao.commit()
    conexao.close()

# Listar usuarios
def listarUsuarios() :
    conexao = conectarBanco()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    for usuario in usuarios :
        print(usuario)
    conexao.close
    
# Atualizar usuários
def atualizarUsuario(id, novoNome, novaIdade) :
    conexao = conectarBanco()
    cursor = conexao.cursor()
    cursor.execute('''UPDATE usuarios SET nome = ?, idade = ? WHERE id = ?''', (novoNome,novaIdade,id))
    conexao.commit()
    conexao.close()

# Excluir usuario
def excluirUsuario(id) :
    conexao = conectarBanco()
    cursor = conexao.cursor()
    cursor.execute('''DELETE FROM usuarios WHERE ID = ?''', (id,))
    conexao.commit()
    conexao.close()

# Executar a criação do banco
criarTabela()

# Vamos inserir um usuário
inserirUsuario("Caio", 39)
inserirUsuario("Lucas", 25)
inserirUsuario("Rafael", 20)
inserirUsuario("Leonardo", 35)
inserirUsuario("Nicole", 16)

# Ver dados armazenados
listarUsuarios()

# editar um usuario
atualizarUsuario(1, "Henrique", 66 )

#Excluir usuario
excluirUsuario(4)