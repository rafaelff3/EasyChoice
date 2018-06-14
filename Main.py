# === IMPORTS ===
from firebase import firebase
from flask import Flask, render_template, request
from ast import literal_eval
import json
import copy
from random import randint
# =============================================================================


# === FIREBASE ===

firebase = firebase.FirebaseApplication('https://easychoicedsoft.firebaseio.com/', None)

carros = firebase.get('/Carros', None)

celulares = firebase.get('/Celulares', None)

# =============================================================================


# === FUNÇÕES ===

# FUNÇÃO QUE RETORNA O RANKING

def retornarank(lista_carros,Espaco_interno,Consumo,Desempenho,Conforto,Seguranca,Custo_beneficio,Desvalorizacao,Manutencao):
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
                pontos += int(carros[marca][modelo][versao]['Manutencao']) * Manutencao
                
                
                ranking['{0} {1} {2}'.format(marca,modelo,versao)] = pontos
                print(pontos)
    print(ranking)
    
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
             desempenho, conforto, seguranca, custo_beneficio, desvalorizacao,manutencao, comentario):
    
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
            'Manutencao': manutencao,
            'Comentario': comentario,
            'Imagem': "bota ae",
            'Opinioes':1
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
                    'Manutencao': manutencao,
                    'Comentario': comentario,
                    'Imagem': "bota ae",
                    'Opinioes':1
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
                conforto,seguranca,custo_beneficio,desvalorizacao,manutencao,comentario):
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
            'Desvalorizacao':(carros[marca][modelo][versao]['Desvalorizacao']+desvalorizacao)/2,
            'Manutencao':(carros[marca][modelo][versao]['Manutencao']+manutencao)/2,
            'Comentario':'{0};{1}'.format(carros[marca][modelo][versao]['Comentario'],comentario),
            'Imagem': carros[marca][modelo][versao]['Imagem'],
            'Opinioes':carros[marca][modelo][versao]['Opinioes'] + 1
            }

    Marca = carros[marca]
    Marca[modelo] = Modelo
    firebase.put('/Carros',marca, Marca)



def filtro(carros,Categoria,Precomin,Precomax):
    lista = copy.deepcopy(carros)
    print(lista)
    for marca in carros.keys():
        for modelo in carros[marca].keys():
            for versao in carros[marca][modelo].keys():
                if carros[marca][modelo][versao]['Preco'] <= Precomax and carros[marca][modelo][versao]['Preco'] >= Precomin:
                    if Categoria != "0":
                        if Categoria != lista[marca][modelo][versao]['Categoria']:
                            del lista[marca][modelo][versao]
                            

                                
                else:
                    del lista[marca][modelo][versao]
    return lista

def filtro_cel(celulares,Precomin,Precomax):
    lista = copy.deepcopy(celulares)
    print(lista)
    for marca in celulares.keys():
        for modelo in celulares[marca].keys():
            if celulares[marca][modelo]['Preco'] > Precomax and celulares[marca][modelo]['Preco'] < Precomin:
                del lista[marca][modelo]
    return lista


def novaopiniao_cel(marca,modelo,preco,acabamento,camera_front,camera_tras,t_carregamento,duracao_bateria,desempenho,custo_beneficio,comentario):
    Marca = celulares[marca]

    Marca[modelo] ={
            'Preco':(celulares[marca][modelo]['Preco']+preco)/2,
            'Acabamento':(celulares[marca][modelo]['Acabamento']+acabamento)/2,
            'Camera frontal':(celulares[marca][modelo]['Camera frontal']+camera_front)/2,
            'Camera traseira':(celulares[marca][modelo]['Camera traseira']+camera_tras)/2,
            'Desempenho':(celulares[marca][modelo]['Desempenho']+desempenho)/2,
            'Tempo de carregamento':(celulares[marca][modelo]['Tempo de carregamento']+t_carregamento)/2,
            'Duracao da bateria':(celulares[marca][modelo]['Duracao da bateria']+duracao_bateria)/2,
            'Custo X Beneficio':(celulares[marca][modelo]['Custo X Beneficio']+custo_beneficio)/2,
            'Comentario':'{0};{1}'.format(celulares[marca][modelo]['Comentario'],comentario),
            'Imagem': celulares[marca][modelo]['Imagem'],
            'Opinioes':celulares[marca][modelo]['Opinioes'] + 1
            }
    
    celulares[marca] = Marca
    firebase.put('/Celulares',marca, Marca)               

def addcel(marca,modelo,preco,acabamento,camera_front,camera_tras,t_carregamento,duracao_bateria,desempenho,custo_beneficio,comentario):
    
    
    if marca in celulares:
        Marca = celulares[marca]
        Marca[modelo] ={
                'Preco':preco,
                'Acabamento':acabamento,
                'Camera frontal':camera_front,
                'Camera traseira':camera_tras,
                'Desempenho':desempenho,
                'Tempo de carregamento':t_carregamento,
                'Duracao da bateria':duracao_bateria,
                'Custo X Beneficio':custo_beneficio,
                'Comentario':comentario,
                'Imagem': "bota ae",
                'Opinioes':1
            }
        celulares[marca] = Marca
    
    else:
        Marca = {}
        Marca[modelo] ={
                'Preco':preco,
                'Acabamento':acabamento,
                'Camera frontal':camera_front,
                'Camera traseira':camera_tras,
                'Desempenho':desempenho,
                'Tempo de carregamento':t_carregamento,
                'Duracao da bateria':duracao_bateria,
                'Custo X Beneficio':custo_beneficio,
                'Comentario':comentario,
                'Imagem': "bota ae",
                'Opinioes':1
                }
        celulares[marca] = Marca 
    
    firebase.put('/Celulares',marca, celulares[marca])
    
def retornarank_cel(lista_celulares,duracao_bateria,desempenho,acabamento,camera_front,camera_tras,custo_beneficio,t_carregamento):
    ranking = {}
    for marca in lista_celulares:
        for modelo in lista_celulares[marca]:

            pontos = 0
            
            pontos += int(celulares[marca][modelo]['Duracao da bateria']) * duracao_bateria
            pontos += int(celulares[marca][modelo]['Desempenho']) * desempenho
            pontos += int(celulares[marca][modelo]['Acabamento']) * acabamento
            pontos += int(celulares[marca][modelo]['Camera frontal']) * camera_front
            pontos += int(celulares[marca][modelo]['Camera traseira']) * camera_tras
            pontos += int(celulares[marca][modelo]['Tempo de carregamento']) * t_carregamento
            pontos += int(celulares[marca][modelo]['Custo X Beneficio']) * custo_beneficio
            
            
            ranking['{0} {1}'.format(marca,modelo)] = pontos
            print(pontos)
    print(ranking)
    
    celular = []
    ponto = []

    for key, value in ranking.items():
        celular.append(key)
        ponto.append(value)

    ranking_final_celular = []
    ranking_final_ponto = []
    
    while len(celular) > 0:
        ranking_final_celular.append(celular[ponto.index(max(ponto))])
        ranking_final_ponto.append(ponto[ponto.index(max(ponto))])
        del celular[ponto.index(max(ponto))]
        del ponto[ponto.index(max(ponto))]
    

    return ranking_final_celular, ranking_final_ponto

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
        Manutencao = int(request.form['manutencao'])
        # Filtra por preco e categoria
        
        lista_carros = filtro(carros,Categoria,Precomin,Precomax)

        ranking, pontos = retornarank(lista_carros,Espaco_interno,Consumo,Desempenho,Conforto,Seguranca,Custo_beneficio,Desvalorizacao,Manutencao)
        
        mensagem_erro = ''
        resul = ''
        
        if len(ranking) == 0:
            mensagem_erro = 'Nenhum carro dessa categoria nessa faixa de preço'
            return render_template('nenhum_carro.html', mensagem_erro=mensagem_erro)
              
        elif len(ranking) > 0:
            resul = ranking[0]
            resulS = resul.split(' ',2)
            comentarios=copy.copy(carros[resulS[0]][resulS[1]][resulS[2]]['Comentario'])
            comentarios=comentarios.split(";")
            imagem = (carros[resulS[0]][resulS[1]][resulS[2]]['Imagem'] != "bota ae")
            Imagem=''
            if imagem:
                Imagem = carros[resulS[0]][resulS[1]][resulS[2]]['Imagem']
            print(Imagem)
            return render_template('ache_seu_carrodpc.html', carros=carros, resul=resul.replace(',','.'), ranking=ranking,resulS=resulS,comentarios=comentarios,imagem=imagem,Imagem=Imagem)
        
    return render_template('ache_seu_carro.html', carros=carros)

@app.route("/carros/ache_seu_carro_prox", methods=['POST','GET'])
def prox_carro():
    rank = request.form['ranking']
    
    ranking = literal_eval(rank)
    
    mensagem_erro = ''
    resul = ''
    del ranking[0]
    
    
    if len(ranking) == 0:
        mensagem_erro = 'Nenhum carro dessa categoria nessa faixa de preço'
        return render_template('nenhum_carro.html', mensagem_erro=mensagem_erro)
    
    elif len(ranking) > 0:
        resul = ranking[0]
        resulS = resul.split(' ',2)
        comentarios=copy.copy(carros[resulS[0]][resulS[1]][resulS[2]]['Comentario'])
        comentarios=comentarios.split(";")
        imagem = (carros[resulS[0]][resulS[1]][resulS[2]]['Imagem'] != "bota ae")
        Imagem=''
        if imagem:
            Imagem = carros[resulS[0]][resulS[1]][resulS[2]]['Imagem']
        return render_template('ache_seu_carrodpc.html', carros=carros, resul=resul.replace(',','.'), ranking=ranking,resulS=resulS,comentarios=comentarios,imagem=imagem,Imagem=Imagem)
    
@app.route("/carros/ache_seu_carro_alea", methods=['POST','GET'])
def alea_carro():
    
    ranking,pontos = retornarank(carros,randint(1,100),randint(1,100),randint(1,100),randint(1,100),randint(1,100),randint(1,100),randint(1,100),randint(1,100))
    
    mensagem_erro = ''
    resul = ''
    
    print('ranking aleatorio:')
    print(ranking)
    print(pontos)
    
    
    if len(ranking) == 0:
        mensagem_erro = 'Nenhum carro dessa categoria nessa faixa de preço'
        return render_template('nenhum_carro.html', mensagem_erro=mensagem_erro)
    
    elif len(ranking) > 0:
        resul = ranking[0]
        resulS = resul.split(' ',2)
        comentarios=copy.copy(carros[resulS[0]][resulS[1]][resulS[2]]['Comentario'])
        comentarios=comentarios.split(";")
        imagem = (carros[resulS[0]][resulS[1]][resulS[2]]['Imagem'] != "bota ae")
        Imagem=''
        if imagem:
            Imagem = carros[resulS[0]][resulS[1]][resulS[2]]['Imagem']
        print(Imagem)
        return render_template('ache_seu_carrodpc.html', carros=carros, resul=resul.replace(',','.'), ranking=ranking,resulS=resulS,comentarios=comentarios,imagem=imagem,Imagem=Imagem)

    
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
        manutencao = int(request.form['manutencao'])
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
            novaopiniao(marca,modelo,versao,float(preco),espaco_interno,consumo,desempenho,conforto,seguranca,custo_beneficio,desvalorizacao,manutencao,comentario)
            return render_template('agradece.html')
                        
                        

    return render_template('nova_opiniao.html', carros=carros, mensagem_erro=mensagem_erro)

# ADICIONA UM NOVO CARRO




@app.route("/carros/add_carro", methods=['GET', 'POST'])
def novo_carro():
    mensagem_erro = ''
    if request.method == 'POST':    
        marca = request.form['marca'].replace(" ","-").upper()
        modelo = request.form['modelo'].replace(" ","-").upper()
        versao = request.form['versao'].upper()
        preco = request.form['preco']
        categoria = request.form['categoria']
        espaco_interno = int(request.form['espaco_interno'])
        consumo = int(request.form['consumo'])
        desempenho = int(request.form['desempenho'])
        conforto = int(request.form['conforto'])
        seguranca = int(request.form['seguranca'])
        custo_beneficio = int(request.form['custo_beneficio'])
        desvalorizacao = int(request.form['desvalorizacao'])
        manutencao = int(request.form['manutencao'])
        comentario = request.form['comentario']        
        
        
        if marca==''or modelo==''or preco==''or categoria=='None' or espaco_interno=='' or consumo==0 or manutencao==0 or desempenho==0 or conforto==0 or seguranca==0 or custo_beneficio==0 or desvalorizacao==0:
            mensagem_erro='Preencha todos os campos'
        
        if versao=='':
            versao = '(Versão única)'
        
        elif marca in carros:
            if modelo in carros[marca]:
                if versao in carros[marca][modelo]:
                    mensagem_erro = 'Esse carro já está no nosso dicionário'
                
                else:
                    addcarro(marca, modelo, versao.replace('.',','), float(preco), categoria, espaco_interno, consumo, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao,manutencao, comentario)
        
                    return render_template('agradece.html')
            
            else:
                addcarro(marca, modelo, versao.replace('.',','), float(preco), categoria, espaco_interno, consumo, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao,manutencao, comentario)
        
                return render_template('agradece.html')
                
        else:
            addcarro(marca, modelo, versao.replace('.',','), float(preco), categoria, espaco_interno, consumo, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao,manutencao, comentario)
        
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


@app.route("/termos",methods=(['POST','GET']))
def priv():
    return render_template('privacidade.html')

# AGRADECE

@app.route("/carros/agradecimento", methods=(['POST','GET']))
def agradece():
    return render_template('agradece.html')

@app.route("/sobre", methods=(['POST','GET']))
def sobre():
    return render_template('sobre.html')


# =============================================================================================



# PÁGINA VIAGENS

@app.route("/viagens", methods=['POST','GET'])    
def pag_viagens():        
    return render_template('viagens.html')


# =============================================================================
    
@app.route("/celulares", methods=['POST','GET'])    
def pag_celulares():        
    return render_template('celulares.html')

@app.route("/celulares/nova_opiniao/marca", methods=['POST','GET'])
def nova_opiniao_celulares_marca():
    mensagem_erro = ''

    if request.method == 'POST':
        marca = request.form['marca']
        if marca!='0': 
            return render_template('nova_opiniao_celulares_modelo.html',celulares=celulares,marca=marca)
        else:
            mensagem_erro = 'Nos diga a marca do seu celular'
    return render_template('nova_opiniao_celulares_marca.html', celulares=celulares, mensagem_erro=mensagem_erro)

@app.route("/celulares/nova_opiniao/marca/modelo", methods=['POST','GET'])
def nova_opiniao_celulares_modelo():
    mensagem_erro = ''

    if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        if modelo!='0':     
            celular = str([marca,modelo])
            return render_template('nova_opiniao_celulares_opinioes.html',celular=celular,celulares=celulares,marca=marca,modelo=modelo)
        else:
            mensagem_erro = 'Nos diga o modelo do seu celular'
    return render_template('nova_opiniao_celulares_modelo.html', celulares=celulares, mensagem_erro=mensagem_erro)

@app.route("/celulares/nova_opiniao/opinioes", methods=['POST','GET'])
def opinioes_cel():
    mensagem_erro = ''
    cel = request.form['celular']
    celular = literal_eval(cel)
    if request.method == 'POST':

        preco = request.form['preco']
        duracao_bateria = int(request.form['duracao_bateria'])
        desempenho = int(request.form['desempenho'])
        acabamento = int(request.form['acabamento'])
        camera_front = int(request.form['camera_front'])
        camera_tras = int(request.form['camera_tras'])
        t_carregamento = int(request.form['t_carregamento'])
        custo_beneficio = int(request.form['custo_beneficio'])
        comentario = request.form['comentario']
        
        
        
        marca = celular[0]
        
        modelo = celular[1]

        
        if preco=='' or duracao_bateria==0  or desempenho==0 or custo_beneficio==0:
            mensagem_erro = 'Preencha todos os campos'
        
        else:
            novaopiniao_cel(marca,modelo,float(preco),acabamento,camera_front,camera_tras,t_carregamento,duracao_bateria,desempenho,custo_beneficio,comentario)
            return render_template('agradece.html')
                        
                        

    return render_template('nova_opiniao.html', celulares=celulares, mensagem_erro=mensagem_erro)

@app.route("/celulares/add_celular", methods=['GET', 'POST'])
def novo_cel():
    mensagem_erro = ''
    if request.method == 'POST':    
        marca = request.form['marca'].replace(" ","-").upper()
        modelo = request.form['modelo'].upper()
        preco = request.form['preco']
        camera_front = int(request.form['camera_front'])
        camera_tras = int(request.form['camera_tras'])
        duracao_bateria = int(request.form['duracao_bateria'])
        desempenho = int(request.form['desempenho'])
        t_carregamento = int(request.form['t_carregamento'])
        acabamento = int(request.form['acabamento'])
        custo_beneficio = int(request.form['custo_beneficio'])
        comentario = request.form['comentario']        
        
        
        if marca in celulares:
            if modelo in celulares[marca]:
                mensagem_erro = 'Esse celular já está no nosso dicionário'
            
            else:
                addcel(marca,modelo,float(preco),acabamento,camera_front,camera_tras,t_carregamento,duracao_bateria,desempenho,custo_beneficio,comentario)
        
                return render_template('agradece.html')
                
        else:
            addcel(marca,modelo,float(preco),acabamento,camera_front,camera_tras,t_carregamento,duracao_bateria,desempenho,custo_beneficio,comentario)
        
            return render_template('agradece.html')
    
    return render_template('novo_celular.html', celulares=celulares, mensagem_erro=mensagem_erro)

@app.route("/celulares/ache_seu_celular", methods=['POST','GET'])
def ache_seu_celular():
    if request.method == 'POST':
        precomin = int(request.form['precomin'])
        precomax = int(request.form['precomax'])
        duracao_bateria = int(request.form['duracao_bateria'])
        desempenho = int(request.form['desempenho'])
        acabamento = int(request.form['acabamento'])
        camera_front = int(request.form['camera_front'])
        camera_tras = int(request.form['camera_tras'])
        t_carregamento = int(request.form['t_carregamento'])
        custo_beneficio = int(request.form['custo_beneficio'])
        # Filtra por preco e categoria
        
        lista_celulares = filtro_cel(celulares,precomin,precomax)

        ranking, pontos = retornarank_cel(lista_celulares,duracao_bateria,desempenho,acabamento,camera_front,camera_tras,custo_beneficio,t_carregamento)
        
        mensagem_erro = ''
        resul = ''
        
        if len(ranking) == 0:
            mensagem_erro = 'Nenhum celular nessa faixa de preço'
            return render_template('nenhum_celular.html', mensagem_erro=mensagem_erro)
              
        elif len(ranking) > 0:
            resul = ranking[0]
            resulS = resul.split(' ',1)
            comentarios=copy.copy(celulares[resulS[0]][resulS[1]]['Comentario'])
            comentarios=comentarios.split(";")
            imagem = (celulares[resulS[0]][resulS[1]]['Imagem'] != "bota ae")
            Imagem=''
            if imagem:
                Imagem = celulares[resulS[0]][resulS[1]]['Imagem']
            return render_template('ache_seu_celulardpc.html', celulares=celulares, resul=resul.replace(',','.'), ranking=ranking,resulS=resulS,comentarios=comentarios,imagem=imagem,Imagem=Imagem)
        
    return render_template('ache_seu_celular.html', celulares=celulares)

@app.route("/celulares/ache_seu_celular_prox", methods=['POST','GET'])
def prox_cel():
    rank = request.form['ranking']
    
    ranking = literal_eval(rank)
    
    mensagem_erro = ''
    resul = ''
    del ranking[0]
    
    
    if len(ranking) == 0:
        mensagem_erro = 'Nenhum celular nessa faixa de preço'
        return render_template('nenhum_celular.html', mensagem_erro=mensagem_erro)
    
    elif len(ranking) > 0:
        resul = ranking[0]
        resulS = resul.split(' ',1)
        comentarios=copy.copy(celulares[resulS[0]][resulS[1]]['Comentario'])
        comentarios=comentarios.split(";")
        imagem = (celulares[resulS[0]][resulS[1]]['Imagem'] != "bota ae")
        Imagem=''
        if imagem:
            Imagem = celulares[resulS[0]][resulS[1]]['Imagem']
        return render_template('ache_seu_celulardpc.html', celulares=celulares, resul=resul.replace(',','.'), ranking=ranking,resulS=resulS,comentarios=comentarios,imagem=imagem,Imagem=Imagem)
    
@app.route("/celulares/ache_seu_celular_alea", methods=['POST','GET'])
def alea_cel():
    
    ranking, pontos = retornarank_cel(celulares,randint(1,100),randint(1,100),randint(1,100),randint(1,100),randint(1,100),randint(1,100),randint(1,100))
    
    mensagem_erro = ''
    resul = ''
    
    print('ranking aleatorio cel:')
    print(ranking)
    print(pontos)
    
    
    if len(ranking) == 0:
        mensagem_erro = 'Nenhum celular nessa faixa de preço'
        return render_template('nenhum_celular.html', mensagem_erro=mensagem_erro)
    
    elif len(ranking) > 0:
        resul = ranking[0]
        resulS = resul.split(' ',1)
        comentarios=copy.copy(celulares[resulS[0]][resulS[1]]['Comentario'])
        comentarios=comentarios.split(";")
        imagem = (celulares[resulS[0]][resulS[1]]['Imagem'] != "bota ae")
        Imagem=''
        if imagem:
            Imagem = celulares[resulS[0]][resulS[1]][resulS[2]]['Imagem']
        return render_template('ache_seu_celulardpc.html', celulares=celulares, resul=resul.replace(',','.'), ranking=ranking,resulS=resulS,comentarios=comentarios,imagem=imagem,Imagem=Imagem)



# RODA O PROGRAMA
app.run('0.0.0.0', 5002, True)

# =============================================================================











