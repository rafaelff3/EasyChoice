#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 12:41:57 2018

@author: pedrovazquez
"""

########################### INPUTS DO USUARIO QUE DESEJA INFORMAR O SITE SOBRE UM VEICULO ##############################
print("Digite 0 para adicionar informações sobre um veículo: ")
print("Digite 1 para encontrar o carro perfeito para voce: ")
resposta = int(input("Digite o numero de acordo com a sua escolha: "))

if resposta ==  0:
    marca = input("Marca do seu veículo: ")
    marca = marca.lower()
    modelo = input("Modelo do seu veículo: ")
    modelo = modelo.lower()
    versao = input("Versao do seu veículo: ")
    versao = versao.lower()
    preco = int(input("Preço pago no veículo: "))
    categoria = input("Categoria do veículo: ")
    #categoria.lower = categoria
    espaco_interno = int(input("Atribua uma nota de 0 a 5, sendo 0 muito ruim e 5 muito bom, para o espaço interno do veículo: "))
    economia = int(input("Atribua uma nota de 0 a 5, sendo 0 muito ruim e 5 muito bom, para a economia do veículo: "))
    desempenho = int(input("Atribua uma nota de 0 a 5, sendo 0 muito ruim e 5 muito bom, para o desempenho do veículo: "))
    conforto =  int(input("Atribua uma nota de 0 a 5, sendo 0 muito ruim e 5 muito bom, para o conforto do veículo: "))
    seguranca =  int(input("Atribua uma nota de 0 a 5, sendo 0 muito ruim e 5 muito bom, para a seguranca do veículo: "))
    desvalorizacao =  int(input("Atribua uma nota de 0 a 5, sendo 0 muito alta e 5 muito baixa, para a desvalorização do veículo: "))
    comentario = input("Adicione um comentário em relação a suas esperiencias com o veículo, seus pontos positivos e negativos: ")
    print(marca, modelo, versao, preco, categoria, espaco_interno, economia, desempenho, conforto, seguranca,desvalorizacao)
######################################## INPUTS DO USUARIO QUE DESEJA ENCONTRAR UM VEICULO #################################
elif resposta == 1:
    print("Primeiramente responda essas questões para que possamos selecionar as melhores opções de carro de acordo com seus interesses")
    preco_minimo = int(input("Preço mínimo: "))
    preco_maximo = int(input("Preço maximo: "))
    categoria_escolhida = input("Escolha a categoria de veículos que mais te apetece, entre hatch-back, sedan, mini-van, perua, conversível, cupê, picape, suv: ")
    categoria_escolhida = categoria_escolhida.lower()
    print("Agora de notas de 0 a 5 para as suas prioridades, sendo 5 muito importante e 0 nada importante: ")
    espaco_interno_nota = int(input("Atribua uma nota de 0 a 5 (sendo 0 pouco importante e 5 muito importante) para o espaço do veículo: "))
    economia_nota= int(input("Atribua uma nota de 0 a 5 (sendo 0 pouco importante e 5 muito importante) para a economia do veículo: "))
    desempenho_nota = int(input("Atribua uma nota de 0 a 5 (sendo 0 pouco importante e 5 muito importante) para o desempenho do veículo: "))
    conforto_nota = int(input("Atribua uma nota de 0 a 5 (sendo 0 pouco importante e 5 muito importante) para o conforto do veículo: "))
    seguranca_nota = int(input("Atribua uma nota de 0 a 5 (sendo 0 pouco importante e 5 muito importante) para a segurança do veículo: "))
    desvalorizacao_nota = int(input("Atribua uma nota de 0 a 5 (sendo 0 pouco importante e 5 muito importante) para a desvalorização do veículo: "))
    
    
    
    
    
    
    
    
    
    
    