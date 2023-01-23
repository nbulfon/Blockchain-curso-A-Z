# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 18:01:21 2023

@author: nicol
"""

# Modulo 1. Crear una Cadena de bloques (Blockchain)

#imports
import datetime
import hashlib
import json
from flask import Flask, jsonify


# Crear la cadena de bloques ->
class Blockchain:
    #{
    #defino el constructor de la clase en python ->
    # en python, c/ metodo va con los dos puntos al final
    def __init__(self):
      #{
       #defino la cadena de bloques que voy a usar ->
       self.chain = []
       # llamo al método, para definir al Bloque Génesis e iniciacizarlo ->
       # le paso el proof of work en 1, y el hash previo, que como es el B. Geneesis, va en 0 ->
       self.create_block(proof = 1, previous_hash = '0')
       #}
       
    # ver que el primer argumento de cualquier funcion es self, para usar las props.
    def create_block(self, proof, previous_hash):
          #defino un diccionario que representa un bloque ->
          # indice, fecha de minado, proof of work,
          block = {
              'index' : len(self.chain)+1, 
              'timestamp' : str(datetime.datetime.now()),
              'proof' : proof,
              'previous_hash' : previous_hash
              }
          self.chain.append(block)
          
          #retorno el bloque, para poder verlo despues en las pruebas desde Postman ->
          return block
    
    # funcion para obtener el último bloque de la cadena.
    def get_previous_block(self):
          return self.chain[-1]
    #}




