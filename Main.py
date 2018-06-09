# === IMPORTS ===
from firebase import firebase
from flask import Flask, render_template, request
from ast import literal_eval
import numpy as np
import json
# =============================================================================


# === FIREBASE ===

firebase = firebase.FirebaseApplication('https://easychoicedsoft.firebaseio.com/', None)

carros = firebase.get('/Carros', None)

# =============================================================================

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
                
                pontos += int(carros[marca][modelo][versao]['Espaco Interno']) * Espaco_interno
                pontos += int(carros[marca][modelo][versao]['Desvalorizacao']) * Desvalorizacao
                pontos += int(carros[marca][modelo][versao]['Consumo']) * Consumo
                pontos += int(carros[marca][modelo][versao]['Desempenho']) * Desempenho
                pontos += int(carros[marca][modelo][versao]['Conforto']) * Conforto
                pontos += int(carros[marca][modelo][versao]['Seguranca']) * Seguranca
                pontos += int(carros[marca][modelo][versao]['Custo X Beneficio']) * Custo_beneficio
                
                
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
    

    return ranking_final_carro, ranking_final_ponto

# FUNÇÃO QUE ADICIONA UM CARRO AO DICIONÁRIO

def addcarro(marca, modelo, versao, preco, categoria, espaco_interno, consumo,
             desempenho, conforto, seguranca, custo_beneficio, desvalorizacao, comentario):
    
    Modelo = {}
    Modelo[versao] ={
            'Preco': preco,
            'Categoria': categoria,
            'Espaco Interno' : espaco_interno,
            'Consumo' : consumo,
            'Desempenho': desempenho,
            'Conforto': conforto,
            'Seguranca': seguranca,
            'Custo X Beneficio': custo_beneficio,
            'Desvalorizacao': desvalorizacao,
            'Comentario': comentario
            }
    
    Marca={}
    Marca[modelo]=Modelo
    if marca in carros:
        if modelo in carros[marca]:
            Modelo = carros[marca][modelo]
            Modelo[versao] ={
                    'Preco': preco,
                    'Categoria': categoria,
                    'Espaco Interno' : espaco_interno,
                    'Consumo' : consumo,
                    'Desempenho': desempenho,
                    'Conforto': conforto,
                    'Seguranca': seguranca,
                    'Custo X Beneficio': custo_beneficio,
                    'Desvalorizacao': desvalorizacao,
                    'Comentario': comentario
                    }
            Marca={}
            Marca[modelo]=Modelo
            Marca = carros[marca]
            Marca[modelo] = Modelo
            carros[marca] = Marca
        else:
            Marca = carros[marca]
            Marca[modelo] = Modelo
            carros[marca] = Marca
    else:
        carros[marca]=Marca
    
    firebase.put('/Carros',marca, carros[marca])
    

def novaopiniao(marca,modelo,versao,preco,espaco_interno,consumo,desempenho,
                conforto,seguranca,custo_beneficio,desvalorizacao,comentario):
    Modelo = carros[marca][modelo]
    Modelo[versao] ={
          'Preco':(carros[marca][modelo][versao]['Preco']+preco)/2,
          'Categoria':carros[marca][modelo][versao]['Categoria'],
          'Espaco Interno':(carros[marca][modelo][versao]['Espaco Interno']+espaco_interno)/2,
          'Consumo':(carros[marca][modelo][versao]['Consumo']+consumo)/2,
          'Desempenho':(carros[marca][modelo][versao]['Desempenho']+desempenho)/2,
          'Conforto':(carros[marca][modelo][versao]['Conforto']+conforto)/2,
          'Seguranca':(carros[marca][modelo][versao]['Seguranca']+seguranca)/2,
          'Custo X Beneficio':(carros[marca][modelo][versao]['Custo X Beneficio']+custo_beneficio)/2,
          'Desvalorizacao':(carros[marca][modelo][versao]['Desvalorizacao']+consumo)/2,
          'Comentario':'{0};{1}'.format(carros[marca][modelo][versao]['Comentario'],comentario)
          }

    Marca = carros[marca]
    Marca[modelo] = Modelo
    firebase.put('/Carros',marca, Marca)



# =============================================================================

# === FLASK ===

app = Flask(__name__)
#firebase=firebase.FirebaseApplication('https://)


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
                    if carros[marca][modelo][versao]['Preco'] <= Precomax and carros[marca][modelo][versao]['Preco'] >= Precomin:
                        if Categoria != "0":
                            if Categoria == carros[marca][modelo][versao]['Categoria']:
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
                            
        ranking, pontos = retornarank(lista_carros,Espaco_interno,Consumo,Desempenho,Conforto,Seguranca,Custo_beneficio,Desvalorizacao)
        
        mensagem_erro = ''
        resul = ''
        
        if len(ranking) == 0:
            mensagem_erro = 'Nenhum carro dessa categoria nessa faixa de preço'
            return render_template('nenhum_carro.html', mensagem_erro=mensagem_erro)
                
        elif len(ranking) > 0:
            resul = ranking[0]
            resulS = resul.split()
        return render_template('ache_seu_carrodpc.html', carros=carros, resul=resul, ranking=ranking,resulS=resulS)
        
    return render_template('ache_seu_carro.html', carros=carros, PRECO=PRECO)



# ADICIONA NOVA OPINIÃO

@app.route("/carros/nova_opiniao/marca", methods=['POST','GET'])
def nova_opiniao_marca():
    mensagem_erro = ''

    if request.method == 'POST':
        marca = request.form['marca']
        if marca!='0':            
            return render_template('nova_opiniao_modelo.html',carros=carros,marca=marca)
        else:
            mensagem_erro = 'Nos diga a marca do seu carro'
    return render_template('nova_opiniao.html', carros=carros, mensagem_erro=mensagem_erro)

@app.route("/carros/nova_opiniao/marca/modelo", methods=['POST','GET'])
def nova_opiniao_modelo():
    mensagem_erro = ''

    if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        if modelo!='0':            
            return render_template('nova_opiniao_versao.html',carros=carros,marca=marca,modelo=modelo)
        else:
            mensagem_erro = 'Nos diga o modelo do seu carro'
    return render_template('nova_opiniao_modelo.html', carros=carros, mensagem_erro=mensagem_erro)

@app.route("/carros/nova_opiniao/marca/modelo/versao", methods=['POST','GET'])
def nova_opiniao_versao():
    mensagem_erro = ''

    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        versao = request.form['versao']
        if versao!='0' and marca!='0' and modelo!='0':
            print(versao)
            print(marca)
            print(modelo)
            print('asdfgdsaASDF')
            carro = str([marca,modelo,versao])
            return render_template('nova_opiniao_opinioes.html',carros=carros,carro=carro,marca=marca,modelo=modelo,versao=versao)
        else:
            mensagem_erro = 'Nos diga a versão do seu carro'
    return render_template('nova_opiniao_versao.html', carros=carros, mensagem_erro=mensagem_erro)





@app.route("/carros/nova_opiniao/opinioes", methods=['POST','GET'])
def opinioes():
    mensagem_erro = ''
    car = request.form['carro']
    carro = literal_eval(car)
    if request.method == 'POST':

        preco = request.form['preco']
        espaco_interno = int(request.form['espaco_interno'])
        consumo = int(request.form['consumo'])
        desempenho = int(request.form['desempenho'])
        conforto = int(request.form['conforto'])
        seguranca = int(request.form['seguranca'])
        custo_beneficio = int(request.form['custo_beneficio'])
        desvalorizacao = int(request.form['desvalorizacao'])
        comentario = request.form['comentario']
        
        marca = carro[0]
        print('Marmelada')
        print(carro)
        print(marca)
        
        modelo = carro[1]
        versao = carro[2]
        
        if preco=='' or espaco_interno==0 or consumo==0 or desempenho==0 or conforto==0 or seguranca==0 or custo_beneficio==0 or desvalorizacao==0:
            mensagem_erro = 'Preencha todos os campos'
        
        else:
            novaopiniao(marca,modelo,versao,float(preco),espaco_interno,consumo,desempenho,conforto,seguranca,custo_beneficio,desvalorizacao,comentario)
            return render_template('agradece.html')
                        
                        

    return render_template('nova_opiniao.html', carros=carros, mensagem_erro=mensagem_erro)

# ADICIONA UM NOVO CARRO




@app.route("/carros/add_carro", methods=['GET', 'POST'])
def novo_carro():
    mensagem_erro = ''
    if request.method == 'POST':    
        marca = request.form['marca']
        modelo = request.form['modelo']
        versao = request.form['versao']
        preco = request.form['preco']
        categoria = request.form['categoria']
        espaco_interno = int(request.form['espaco_interno'])
        consumo = int(request.form['consumo'])
        desempenho = int(request.form['desempenho'])
        conforto = int(request.form['conforto'])
        seguranca = int(request.form['seguranca'])
        custo_beneficio = int(request.form['custo_beneficio'])
        desvalorizacao = int(request.form['desvalorizacao'])
        comentario = request.form['comentario']        
        
        if marca==''or modelo==''or versao==''or preco==''or categoria=='None' or espaco_interno==0 or consumo==0 or desempenho==0 or conforto==0 or seguranca==0 or custo_beneficio==0 or desvalorizacao==0:
            mensagem_erro='Preencha todos os campos'
        
        elif marca in carros:
            if modelo in carros[marca]:
                if versao in carros[marca][modelo]:
                    mensagem_erro = 'Esse carro já está no nosso dicionário'
                
                else:
                    addcarro(marca, modelo, versao, float(preco), categoria, espaco_interno, consumo, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao, comentario)
        
                    return render_template('agradece.html')
            
            else:
                addcarro(marca, modelo, versao, float(preco), categoria, espaco_interno, consumo, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao, comentario)
        
                return render_template('agradece.html')
                
        else:
            addcarro(marca, modelo, versao, float(preco), categoria, espaco_interno, consumo, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao, comentario)
        
            return render_template('agradece.html')
    
    return render_template('novo_carro.html', carros=carros, mensagem_erro=mensagem_erro)

# DENUNCIA ERRO
@app.route("/comunicar",methods=(['POST','GET']))
def comunicar():
    if request.method == 'POST':
        with open('erros.json','r') as dados:
            erros = json.load(dados)
        erro = request.form['erro']
        
        
        
        erros.append(erro)
        with open('erros.json','w') as dados:
            erros_novos = json.dumps(erros)
            dados.write(erros_novos)
        return render_template('agradece.html')
        
    return render_template('comunicar.html')



# AGRADECE

@app.route("/carros/agradecimento", methods=(['POST','GET']))
def agradece():
    return render_template('agradece.html')
    
# RODA O PROGRAMA
app.run('0.0.0.0', 5000, True)

# =============================================================================











