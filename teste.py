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
carros = {
  "VW": {
    "Fox": {
      "MPI 1.0": Carros(55000,"hatchback",4,3,2,2,4,3,4,["Bem loco"]),
      "MPI 1.6": Carros(70000,"hatchback",4,3,2,2,4,3,5,["Bem loco"])
    }
  },
  "Honda": {
    "Civic": {
      "SI" : Carros(160000,"cupe",3,3,5,4,4,2,3,["Carin q só"])
    }
  },
}



def addcarro(marca, modelo, versao, preco, categoria, espaco_interno, consumo, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao, comentario):
    #carros[marca][modelo][versao] = Carros(preco, categoria, espaco_interno, consumo, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao, comentario)
    Modelo = {}
    Modelo[versao] = Carros(preco, categoria, espaco_interno, consumo, desempenho, conforto, seguranca, custo_beneficio, desvalorizacao, comentario)
    Marca = {}
    Marca[modelo] = Modelo
    carros[marca] = Marca
addcarro('VW','Golf','1.0',120000,'hatchback',3,3,3,3,3,3,3,'asdf')

print(carros)

        