# imports
from flask import Flask, render_template, request, redirect, url_for
from ast import literal_eval

app = Flask(__name__)

# Classes

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
        self.comentario = comentario
    pass

# Funções
def retornarank(lista_carros,espaco_interno,consumo,desempenho,conforto,seguranca,custo_beneficio,desvalorizacao):
    ranking = {}
    for marca in lista_carros:
        for modelo in lista_carros[marca]:
            for versao in lista_carros[marca][modelo]:
                pontos = 0
                
                pontos += int(lista_carros[marca][modelo][versao].espaco_interno)*espaco_interno
                pontos += int(lista_carros[marca][modelo][versao].consumo)*consumo
                pontos += int(lista_carros[marca][modelo][versao].desempenho)*desempenho
                pontos += int(lista_carros[marca][modelo][versao].conforto)*conforto
                pontos += int(lista_carros[marca][modelo][versao].seguranca)*seguranca
                pontos += int(lista_carros[marca][modelo][versao].custo_beneficio)*custo_beneficio
                pontos += int(lista_carros[marca][modelo][versao].desvalorizacao)*desvalorizacao
                
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
    
    
    return ranking_final_carro, ranking_final_ponto
    
        
        

# Lista de carros

carros = {
  "VW": {
    "Fox": {
      "1.0": Carros(55000,"hatchback",4,3,2,2,4,3,4,"Bem loco"),
      "1.6": Carros(70000,"hatchback",4,3,2,2,4,3,4,"Bem loco")
    }
  },
  "Honda": {
    "Civic": {
      "SI" : Carros(160000,"cupe",3,3,5,4,4,2,3,"Carin q só")
    }
  },
}

# Função principal
@app.route("/", methods=['POST','GET'])    
def pagina_inicial():
    if request.method == 'POST':
        
        onde = request.form['onde']
        
        if onde == 'busca':
            return redirect("/ache_seu_carro", code=302)
        
        elif onde == 'novo':
            return redirect("/nova_opiniao", code=302)
        
    return render_template('pagprin.html')

@app.route("/ache_seu_carro", methods=['POST','GET'])
def ache_seu_carro():    
    mensagem_erro = ''
    if request.method == 'POST':
        precomin = float(request.form['precomin'])
        precomax = float(request.form['precomax'])
        categoria = request.form['categoria']
        espaco_interno = int(request.form['espaco_interno'])
        consumo = int(request.form['consumo'])
        desempenho = int(request.form['desempenho'])
        conforto = int(request.form['conforto'])
        seguranca = int(request.form['seguranca'])
        custo_beneficio = int(request.form['custo_beneficio'])
        desvalorizacao = int(request.form['desvalorizacao'])
        
        lista_carros = {}
        for key,value in carros.items():
            
            lista_carros[key] = value
        
        # Filtra por preco
        
        for marca in carros:
            for modelo in carros[marca]:
                for versao in carros[marca][modelo]:
                    if carros[marca][modelo][versao].preco > precomax or carros[marca][modelo][versao].preco < precomin:
                        del lista_carros[marca][modelo][versao]
        
        # Filtra por categoria                
        
        for marca in carros:
            for modelo in carros[marca]:
                for versao in carros[marca][modelo]:                    
                    if carros[marca][modelo][versao].categoria != categoria and categoria != "0":
                        del lista_carros[marca][modelo][versao]
        
        #### erro ao filtrar, ele diz que a lista esta mudando de tamanho
        
        ranking, pontos = retornarank(lista_carros,espaco_interno,consumo,desempenho,conforto,seguranca,custo_beneficio,desvalorizacao)
        
        with open('ranking.py','w') as dados:
            dados.write(str(ranking))
        
        return redirect("/ache_seu_carro/dpc", code=302)
        
    return render_template('Limpo.html', carros=carros, mensagem_erro=mensagem_erro)

@app.route("/ache_seu_carro/dpc", methods=['POST','GET'])
def dpc():
    mensagem_erro = ''
    resul = ''
    
    with open('ranking.py','r') as dados:
        ranking = literal_eval(dados.read())
        
    if len(ranking) == 0:
        mensagem_erro = 'Nenhum carro dessa categoria nessa faixa de preço'
                
    elif len(ranking) > 0:
        resul = 'O carro ideal para você: {0}'.format(ranking[0])
            
    return render_template('Limpodpc.html', carros=carros, mensagem_erro=mensagem_erro, resul=resul)

@app.route("/nova_opiniao", methods=(['POST','GET']))
def nova_opiniao():
    if request.method == 'POST':
        #c = request.method["vai"]
        
        c = "false"
        
        if c == "false":
            return 'aaaaaaa' 
            return redirect("/add_carro", code=302)
        
        
        

           
    return render_template('nova_opiniao.html', carros=carros)

@app.route("/add_carro", methods=(['POST','GET']))
def novo_carro():
    return 'ok'
# Adiciona carro novo

def addcarro(marca, modelo, versao, preco, categoria, espaco_interno, economia, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao):
    carros["carros"][modelo][versao] = Carros(preco, categoria, espaco_interno, economia, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao)

app.run('0.0.0.0', 5004, True)




'''
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
'''