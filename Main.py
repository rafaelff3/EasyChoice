# =========================== SUMÁRIO =========================================




# === IMPORTS ===

from flask import Flask, render_template, request, redirect
from ast import literal_eval
import numpy as np

# =============================================================================


# === CLASSES ===

# CLASSE DOS CARROS

class Carros(): #objeto
    def __init__(self,preco,categoria,espaco_interno,consumo,desempenho,conforto,seguranca,custo_beneficio,desvalorizacao,comentario):
        self.preco = preco
        self.categoria = categoria
        self.espaco_interno = espaco_interno
        self.consumo = consumo
        self.desempenho  = desempenho
        self.conforto = conforto 
        self.seguranca = seguranca
        self.custo_beneficio = custo_beneficio
        self.desvalorizacao = desvalorizacao
        self.comentario = [comentario]
    pass

PRECO = np.arange(0,300000,2500)

# =============================================================================


# === FUNÇÕES ===

# FUNÇÃO QUE RETORNA O RANKING

def retornarank(lista_carros,Espaco_interno,Consumo,Desempenho,Conforto,Seguranca,Custo_beneficio,Desvalorizacao):
    ranking = {}
    for marca in lista_carros:
        for modelo in lista_carros[marca]:
            for versao in lista_carros[marca][modelo]:
                pontos = 0
                
                pontos += int(lista_carros[marca][modelo][versao].espaco_interno)*Espaco_interno
                pontos += int(lista_carros[marca][modelo][versao].consumo)*Consumo
                pontos += int(lista_carros[marca][modelo][versao].desempenho)*Desempenho
                pontos += int(lista_carros[marca][modelo][versao].conforto)*Conforto
                pontos += int(lista_carros[marca][modelo][versao].seguranca)*Seguranca
                pontos += int(lista_carros[marca][modelo][versao].custo_beneficio)*Custo_beneficio
                pontos += int(lista_carros[marca][modelo][versao].desvalorizacao)*Desvalorizacao
                
                ranking['{0} {1} {2}'.format(marca,modelo,versao)] = pontos
                
                
    carro = []
    ponto = []

    for key, value in ranking.items():
        carro.append(key)
        ponto.append(value)

    ranking_final_carro = []
    ranking_final_ponto = []
    
    while len(carro) > 0:
        ranking_final_carro.append(carro[ponto.index(max(ponto))])
        ranking_final_ponto.append(ponto[ponto.index(max(ponto))])
        del carro[ponto.index(max(ponto))]
        del ponto[ponto.index(max(ponto))]
    
    with open('ranking.py','w') as dados:
        dados.write(str(ranking_final_carro))
    
    return ranking_final_carro, ranking_final_ponto

# FUNÇÃO QUE ADICIONA UM CARRO AO DICIONÁRIO

def addcarro(marca, modelo, versao, preco, categoria, espaco_interno, consumo, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao, comentario):
    #carros[marca][modelo][versao] = Carros(preco, categoria, espaco_interno, consumo, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao, comentario)
    Modelo = {}
    Modelo[versao] = Carros(preco, categoria, espaco_interno, consumo, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao, comentario)
    Marca = {}
    Marca[modelo] = Modelo
    carros[marca] = Marca
# =============================================================================


# === DICIONÁRIO ===
    
carros = {
  "VW": {
    "Fox": {
      "MPI 1.0": Carros(55000,"hatchback",4,3,2,2,4,3,4,["Bem loco"]),
      "MPI 1.6": Carros(70000,"hatchback",4,3,2,2,4,3,4,["Bem loco"])
    }
  },
  "Honda": {
    "Civic": {
      "SI" : Carros(160000,"cupe",3,3,5,4,4,2,3,["Carin q só"])
    }
  },
}


# =============================================================================

# === FLASK ===

app = Flask(__name__)


# PÁGINA PRINCIPAL
@app.route("/", methods=['POST','GET'])
def pagina_principal():
    return render_template('pagina_principal.html')

# PÁGINA CARRO

@app.route("/carros", methods=['POST','GET'])    
def pag_carros():        
    return render_template('carros.html')


# ACHA CARRO

@app.route("/carros/ache_seu_carro", methods=['POST','GET'])
def ache_seu_carro():
    if request.method == 'POST':
        Precomin = float(request.form['precomin'])
        Precomax = float(request.form['precomax'])
        Categoria = request.form['categoria']
        Espaco_interno = int(request.form['espaco_interno'])
        Consumo = int(request.form['consumo'])
        Desempenho = int(request.form['desempenho'])
        Conforto = int(request.form['conforto'])
        Seguranca = int(request.form['seguranca'])
        Custo_beneficio = int(request.form['custo_beneficio'])
        Desvalorizacao = int(request.form['desvalorizacao'])
        
        # Filtra por preco e categoria
        
        lista_carros = {}
        for marca in carros:
            for modelo in carros[marca]:
                for versao in carros[marca][modelo]:
                    if carros[marca][modelo][versao].preco <= Precomax and carros[marca][modelo][versao].preco >= Precomin:
                        if Categoria != "0":
                            if Categoria == carros[marca][modelo][versao].categoria:
                                Modelo = {}
                                Modelo[versao] = carros[marca][modelo][versao]
                                Marca = {}
                                Marca[modelo] = Modelo
                                lista_carros[marca] = Marca
                        else:
                            Modelo = {}
                            Modelo[versao] = carros[marca][modelo][versao]
                            Marca = {}
                            Marca[modelo] = Modelo
                            lista_carros[marca] = Marca
        #### erro ao filtrar, ele diz que a lista esta mudando de tamanho
        
        ranking, pontos = retornarank(lista_carros,Espaco_interno,Consumo,Desempenho,Conforto,Seguranca,Custo_beneficio,Desvalorizacao)
        
        return redirect("/carros/ache_seu_carro/dpc", code=302)
        
    return render_template('ache_seu_carro.html', carros=carros, PRECO=PRECO)


# RETORNA O MELHOR CARRO

@app.route("/carros/ache_seu_carro/dpc", methods=['POST','GET'])
def dpc():
    mensagem_erro = ''
    resul = ''
    
    with open('ranking.py','r') as dados:
        ranking = literal_eval(dados.read())
        
    if len(ranking) == 0:
        mensagem_erro = 'Nenhum carro dessa categoria nessa faixa de preço'
                
    elif len(ranking) > 0:
        resul = 'O carro ideal para você: {0}'.format(ranking[0])
        
    return render_template('ache_seu_carrodpc.html', carros=carros, mensagem_erro=mensagem_erro, resul=resul)


# ADICIONA NOVA OPINIÃO

@app.route("/carros/nova_opiniao", methods=(['POST','GET']))
def nova_opiniao():
    c = False
    Mar = []
    Mod = []
    Ver = []
    mensagem_erro = ''
    if request.method == 'POST':
        marca = request.form['marca']
        if marca != '0':
            modelo = request.form['modelo']
            if modelo !='0':
                versao = request.form['versao']
                if versao !='0':
                    if marca!='0' and modelo!='0' and versao!='0':
                        Mar.append(marca)
                        Mod.append(modelo)
                        Ver.append(versao)
                        c = True
                        preco = float(request.form['preco'])
                        espaco_interno = int(request.form['espaco_interno'])
                        consumo = int(request.form['consumo'])
                        desempenho = int(request.form['desempenho'])
                        conforto = int(request.form['conforto'])
                        seguranca = int(request.form['seguranca'])
                        custo_beneficio = int(request.form['custo_beneficio'])
                        desvalorizacao = int(request.form['desvalorizacao'])
                        comentario = request.form['comentario']
                        
                        carros[marca][modelo][versao] = Carros((carros[marca][modelo][versao].preco + preco)/2,carros[marca][modelo][versao].categoria,(carros[marca][modelo][versao].espaco_interno + espaco_interno)/2,(carros[marca][modelo][versao].consumo + consumo)/2,(carros[marca][modelo][versao].desempenho + desempenho)/2,(carros[marca][modelo][versao].conforto + conforto)/2,(carros[marca][modelo][versao].seguranca + seguranca)/2,(carros[marca][modelo][versao].custo_beneficio + custo_beneficio)/2,(carros[marca][modelo][versao].desvalorizacao + desvalorizacao)/2,carros[marca][modelo][versao].comentario.append(comentario))
                        #return redirect("/carros/agradecimento", code=302)
                    else:
                        mensagem_erro = 'Preencha todos os campos'
                else:
                    mensagem_erro = 'Preencha todos os campos'
            else:
                mensagem_erro = 'Preencha todos os campos'
        else:
            mensagem_erro = 'Preencha todos os campos'
    return render_template('nova_opiniao.html', carros=carros, mensagem_erro=mensagem_erro, c=c)


# ADICIONA UM NOVO CARRO

@app.route("/carros/add_carro", methods=['GET', 'POST'])
def novo_carro():
    if request.method == 'POST':    
        marca = request.form['marca']
        modelo = request.form['modelo']
        versao = request.form['versao']
        preco = float(request.form['preco'])
        categoria = request.form['categoria']
        espaco_interno = int(request.form['espaco_interno'])
        consumo = int(request.form['consumo'])
        desempenho = int(request.form['desempenho'])
        conforto = int(request.form['conforto'])
        seguranca = int(request.form['seguranca'])
        custo_beneficio = int(request.form['custo_beneficio'])
        desvalorizacao = int(request.form['desvalorizacao'])
        comentario = request.form['comentario']        

        addcarro(marca, modelo, versao, preco, categoria, espaco_interno, consumo, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao, comentario)
        
        return render_template('agradece.html')
    
    return render_template('novo_carro.html', carros=carros)


# AGRADECE

@app.route("/carros/agradecimento", methods=(['POST','GET']))
def agradece():
    return render_template('agradece.html')
    

# RODA O PROGRAMA
app.run('0.0.0.0', 5007, True)

# =============================================================================











