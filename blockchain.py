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


# Parte 1: Crear la cadena de bloques ->
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
      
    # funcion proof of work, recibo el self, y la proof anterior para generar el problema siguiente.
    def proof_of_work(self, previous_proof):
        new_proof = 1
        # si check_proof es true, el minero hallo la colucion.
        check_proof = False
        
        # mientras no esté resuelta la prueba...
        # cuantos mas ceros le exiga a la proof of work, mas complicado será para el minero, porque deberá pasar más iteraciones para llegar al hash indicado...
        while check_proof is False:
            # exigo que no sea simetrico el hash ->
            # le paso como argumento una ecuacion que represente un reto para el minero ->
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            #checkeo que hayan 4 ceros al inicio (en este caso) ->
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    # funcion de para generar un hash de un bloque
    def hash(self, block):
        # primero, convierto a string codificado el bloque, asi lo suministro a el algoritmo sha256 ->
        # le paso el bloque que quiero codificar, y le digo que ordene los datos del diccionario, para prevenir asi, el Efecto Avalancha ->
        encode_block = json.dumps(block, sort_keys = True).encode()
        # el .hexdigest() es para convertirlo en hexadecimal.
        return hashlib.sha256(encode_block).hexdigest()
    #}

# Parte 2 - Minado de un bloque de la cadena



