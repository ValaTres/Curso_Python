#     _    ___ ____    ____  _     _                           
#    / \  |_ _/ ___|  / ___|(_)___| |_ ___ _ __ ___   __ _ ___ 
#   / _ \  | |\___ \  \___ \| / __| __/ _ \ '_ ` _ \ / _` / __|
#  / ___ \ | | ___) |  ___) | \__ \ ||  __/ | | | | | (_| \__ \
# /_/   \_\___|____/  |____/|_|___/\__\___|_| |_| |_|\__,_|___/

#Autor: Lucas S Ferreira
#Versão: 0.1.0

from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import sqlite3
import os
import config
import numpy as np
import dash
from dash import Dash, html, dcc
import plotly.graph_objs as go

app = Flask(__name__)
db_path = config.DB_PATH

# Função para inicializar o banco de dados
def init_db() :
    with sqlite3.connect('db.path') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inadimplencia(
                mes TEXT PRIMARY KEY,
                inadimplencia REAL
            )               
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selic(
            mes TEXT PRIMARY KEY,
            selic_diaria REAL
            )
        ''')
        conn.commit()
        
@app.route('/')
def index():
    return render_template_string('''
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f4f8;
            color: #344054;
            padding: 40px;
        }

        .container {
            max-width: 550px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px #00000010;
        }

        h1 { color: #24476b; text-align: center; }
        label { display: block; margin: 15px 0 8px; }
        input { margin-bottom: 10px; }
        input[type="submit"] {
            background: #315f85; color: white; border: none;
            padding: 11px 22px; border-radius: 6px; cursor: pointer;
        }
        input[type="submit"]:hover { background: #24476b; }
        a { display: block; color: #315f85; text-decoration: none; margin: 12px 0; }
        a:hover { color: #172f48; text-decoration: underline; }
        hr { border: 0; border-top: 1px solid #e5eaf0; margin: 25px 0; }
    </style>

    <div class="container">
        <h1>Upload de Dados Econômicos</h1>

        <form action="/upload" method="POST" enctype="multipart/form-data">
            <label for="campo_inadimplencia">Arquivo de Inadimplência (CSV):</label>
            <input name="campo_inadimplencia" id="campo_inadimplencia" type="file" required>

            <label for="campo_selic">Arquivo da Taxa Selic (CSV):</label>
            <input name="campo_selic" id="campo_selic" type="file" required>

            <br><br>
            <input type="submit" value="Fazer Upload">
        </form>

        <hr>

        <a href="/consultar">Consultar dados armazenados</a>
        <a href="/graficos">Visualizar gráficos</a>
        <a href="/editar_inadimplencia">Editar dados de inadimplência</a>
        <a href="/editar_selic">Editar dados de selic</a>
        <a href="/correlacao">Analisar correlação</a>
    </div>
    ''')
    
@app.route('/upload', methods=['POST','GET'])
def upload():
    inad_file = request.files.get('campo_inadimplencia')
    selic_file = request.files.get('campo_selic')

    # Vamos verificar se os arquivos foram devidamente enviados
    if not inad_file or not selic_file:
        return jsonify({'ERRO':'AMBOS OS ARQUIVOS PRECISAM SER ENVIADOS!'})
    inad_df = pd.read_csv(
        inad_file,
        sep = ";",
        names = ['data', 'inadimplencia'],
        header = 0
    )
    selic_df = pd.read_csv(
        selic_file,
        sep = ";",
        names = ['data', 'selic_diaria'],
        header = 0
    )
    
    inad_df['data'] = pd.to_datetime(inad_df['data'], format = "%d/%m/%Y")
    selic_df['data'] = pd.to_datetime(selic_df['data'], format = "%d/%m/%Y")
    
    inad_df['mes'] = inad_df['data'].dt.to_period('M').astype(str)
    selic_df['mes'] = selic_df['data'].dt.to_period('M').astype(str)
    
    inad_mensal = inad_df [['mes','inadimplencia']].drop_duplicates()
    selic_mensal = selic_df.groupby('mes')['selic_diaria'].mean().reset_index()

    with sqlite3.connect(db_path) as conn:
        inad_mensal.to_sql('inadimplencia', conn, if_exists='replace', index = False)
        selic_mensal.to_sql('selic', conn, if_exists='replace', index = False)
    return jsonify({'Mensagem ':'Dados armazenados com sucesso!'})  

@app.route('/consultar', methods=['POST','GET'])
def consultar() :
    
    # Resultado se a pagina for carregada recebendo um POST
    if request.method == 'POST':
        tabela = request.form.get('campo_tabela')
        if tabela not in ['inadimplencia','selic']:
            return jsonify({'Erro':'Tabela invalida'}),400
        with sqlite3.connect(db_path) as conn :
            df = pd.read_sql_query(f'SELECT * FROM {tabela}', conn)
        return df.to_html(index=False)
        
    #Resultado sem receber um POST, ou seja, primeiro carregamento da pagina
    return render_template_string('''
        <h1> Consulta de Tabelas </h1>
        <form method='POST'>
            <label for='campo_tabela'> Escolha uma Tabela: <label>
            <select name='campo_tabela'>
                <option value='inadimplencia'> Inadimplencia </option>
                <option value='selic'> Taxa Selic </option>
            <select>
            <input type="submit" value="consultar">
        </form>
        <br><a  href="/"> Voltar </a>                              
    ''')

@app.route('/graficos')
def graficos():
    with sqlite3.connect(db_path) as conn :
        inad_df = pd.read_sql_query('SELECT * FROM inadimplencia', conn)
        selic_df = pd.read_sql_query('SELECT * FROM selic', conn)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x = inad_df['mes'],
        y = inad_df['inadimplencia'],
        mode = 'lines+markers',
        name = 'inadimplência'
        )
    )
    fig1.update_layout(
        title = 'Evolução da Inadimplência',
        xaxis_title = 'Mês',
        yaxis_title = '%',
        template = 'plotly_dark'
        #'ggplot2', 'seaborn', 'simple_white', 'plotly','plotly_white', 'plotly_dark', 
        #'presentation', 'xgridoff','ygridoff', 'gridon', 'none'
    )
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x = selic_df['mes'],
        y = selic_df['selic_diaria'],
        mode = 'lines+markers',
        name = 'selic'
        )
    )
    fig2.update_layout(
        title = 'Média Mensal da Selic',
        xaxis_title = 'Mês',
        yaxis_title = 'Taxa',
        template = 'plotly_dark'
    )
    graph_html_1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')
    graph_html_2 = fig2.to_html(full_html=False, include_plotlyjs='False')
    
    return render_template_string('''
        <html>
            <head>
                <title> Graficos Esconomicos </title>
                <style>
                        .container{
                            display:flex;
                            justify-content:space-around;
                        }
                        .graph{ 
                            width: 48%;
                        }      
                </style>
            </head>
            <body>
                <h1> Graficos Economicos </h1>   
                    <div class="container">                    
                        <div class="graph">{{ grafico1|safe }}</div>
                        <div class="graph">{{ grafico2|safe }}</div>
                    </div>            
            </body>
        </html>                             
    ''', grafico1 = graph_html_1, grafico2 = graph_html_2)

@app.route('/editar_inadimplencia', methods=['POST', 'GET'])
def editar_inadimplencia():
    if request.method == 'POST':
        mes = request.form.get('campo_mes')
        novo_valor = request.form.get('campo_valor')
        try:
            novo_valor = float(novo_valor)
        except:
            return jsonify({'Erro': 'Valor invalido'})
        #
        #SEPARADO PARA TRATAMENTO DE DADOS
        #
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE inadimplencia SET inadimplencia = ? WHERE mes = ?', (novo_valor, mes))
        return jsonify({'Mensagem': f'Valor atualizado para o mes de {mes} com sucesso'})
    return render_template_string('''
    <h1> Editar Inadimplencia </h1>
        <form method="POST" action="/editar_inadimplencia">
            <label for="campo_mes">Mês (AAAA-MM):</label>
            <input type="text" name="campo_mes"><br>
                                  
            <label for="campo_valor">Novo valor de Inadimplência:</label>
            <input type="text" name="campo_valor"><br>
                                  
            <input type="submit" value="Atualizar Dados">
        </form>
        <br>
        <a href="/"> Voltar </a>
    ''')
    
@app.route('/editar_selic', methods=['POST', 'GET'])
def editar_selic():
    if request.method == 'POST':
        mes = request.form.get('campo_mes')
        novo_valor = request.form.get('campo_valor')
        try:
            novo_valor = float(novo_valor)
        except:
            return jsonify({'Erro':'Valor invalido'}),400
        #
        #SEPARADO PRA TRATAMENTO DE ERROS
        #
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE selic SET selic_diaria = ? WHERE mes = ?', (novo_valor, mes))
            conn.commit()
        
            if cursor.rowcount == 0:
                return jsonify({'Erro':f'Não foi possivel encontrar o registro para op {mes}'}), 404
        return jsonify({'Mensagem':f'Taxa taxa atualizada para o {mes} com sucesso'})
    return render_template_string('''
            <h1>Editar Taxa SELIC</h1>
            <form method="POST" action="/editar_selic">
                <label for="campo_mes">Mês (AAAA-MM):</label>
                <input name="campo_mes" required>
                <br><br>
                <label for="campo_valor">Nova Taxa SELIC:</label>
                <input name="campo_valor">
                <br><br>
                <input type="submit" value="Atualizar Dados">
            </form>
            <br>
            <a href="/">Voltar</a>                        
    ''')
    
    
    return render_template_string('''
    <h1> Editar Selic </h1>
            <form method="POST" action="/editar_selic">
                <label for="campo_mes">Mês (AAAA-MM):</label>
                <input type="text" name="campo_mes"><br>
                                        
                <label for="campo_valor">Novo valor de Selic:</label>
                <input type="text" name="campo_valor"><br>
                                        
                <input type="submit" value="Atualizar Selic">
            </form>
            <br>
            <a href="/"> Voltar </a>
    ''')
if __name__ == '__main__':
    init_db()
    app.run(debug=True)