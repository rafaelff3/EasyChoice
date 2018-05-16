# imports
from flask import Flask, render_template, request
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
                
                
    ranking_final = []
    while len(ranking) > 0:
        for marca in lista_carros:
            for modelo in carros[marca]:
                for versao in carros[marca][modelo]:
                    
                        ranking_final.append()
        
        
        

# Lista de carros

carros = {
  "VW": {
    "Fox": {
      "1.0": 1,
      "1.6": 1
  },
}}

# Função principal
@app.route("/", methods=['POST','GET'])
def pagina_inicial():    
    mensagem_erro = ''
    if request.method == 'POST':
        precomin = request.form['precomin']
        precomax = request.form['precomax']
        categoria = request.form['categoria']
        espaco_interno = request.form['espaco_interno']
        consumo = request.form['consumo']
        desempenho = request.form['desempenho']
        conforto = request.form['conforto']
        seguranca = request.form['seguranca']
        custo_beneficio = request.form['custo_beneficio']
        desvalorizacao = request.form['desvalorizacao']
        
        lista_carros = []
        for i in carros:
            lista_carros.append(i)
        
        # Filtra por preco
        
        for marca in lista_carros:
            for modelo in carros[marca]:
                for versao in carros[marca][modelo]:
                    if carros[marca][modelo][versao].preco > precomax or carros[marca][modelo][versao].preco < precomin:
                        del lista_carros[marca][modelo][versao]
        
        # Filtra por categoria                
        
        for marca in lista_carros:
            for modelo in carros[marca]:
                for versao in carros[marca][modelo]:                    
                    if carros[marca][modelo][versao].categoria != categoria and categoria != "0":
                        del lista_carros[marca][modelo][versao]
        
        
        
    return render_template('Limpo.html', carros=carros, mensagem_erro=mensagem_erro)    


# Adiciona carro novo

def addcarro(marca, modelo, versao, preco, categoria, espaco_interno, economia, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao):
    carros["carros"][modelo][versao] = Carros(preco, categoria, espaco_interno, economia, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao)

app.run('0.0.0.0', 5001, True)