import json




with open('erros.json','r') as dados:
    erros = json.load(dados)

print(erros)

erros.append('erro')

with open('erros.json','w') as dados:
    erros_novos = json.dumps(erros)
    dados.write(erros_novos)
            