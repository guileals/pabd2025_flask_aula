from flask import Flask, render_template, redirect, request, url_for
from datetime import datetime
from config.database import SupabaseConnection
from dao.funcionario_dao import FuncionarioDAO

app = Flask(__name__)

client = SupabaseConnection().client

# Criando DAO para acessar a tabela funcionario
funcionario_dao = FuncionarioDAO(client)

# Filtro personalizado para formatar CPF
@app.template_filter('format_cpf')
def format_cpf(cpf):
    """Formata CPF no padrão XXX.XXX.XXX-XX"""
    if not cpf or len(cpf) != 11:
        return cpf
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"

@app.route("/")
def index():
    return render_template("index.html", title="3INF1M", app_name="Meu Flask App", funcionarios=funcionario_dao.read_all())

@app.route("/funcionario/<string:pk>/<int:id>")
def details(pk, id):
    funcionario = funcionario_dao.read(pk, id)
    return render_template("details.html", funcionario=funcionario, datetime=datetime)

### Verifica se rota é GET ou POST para atualizar funcionário
@app.route('/funcionario/edit/<string:pk>', methods=['GET', 'POST'])
def update(pk):
    # Se for POST (ou seja, envio do formulário)
    if request.method == 'POST':
        ###
        # Aqui acontece a mágica - atualiza funcionário
        ###
        return redirect(url_for('index'))
    
    # Se for GET, apenas exibe o formulário com os dados atuais
    funcionario = funcionario_dao.read('cpf', pk)
    return render_template('edit.html', funcionario=funcionario, datetime=datetime)

### Verifica se rota é GET ou POST para remover funcionário
@app.route('/funcionario/delete/<string:pk>', methods=['GET', 'POST'])
def delete(pk):
    # Se for POST (ou seja, envio do formulário)
    if request.method == 'POST':
        ###
        # Aqui acontece a mágica - exclui funcionário
        ###
        return redirect(url_for('index'))
    
    # Se for GET, apenas exibe o funcionário a ser removido
    funcionario = funcionario_dao.read('cpf', pk)
    return render_template('delete.html', funcionario=funcionario, datetime=datetime)

