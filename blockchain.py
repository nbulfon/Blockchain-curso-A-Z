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
            ecuacion = (new_proof**2 - previous_proof**2)
            hash_operation = hashlib.sha256(str(ecuacion).encode()).hexdigest()
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
    
    # funcion para verificar si la cadena de bloques es válida.
    def is_chain_valid(self, chain):
        # inicializo en qué posicion voy a empezar (el bloque genesis) ->
        previous_block = chain[0]
        # inicicializo la posicion en la que estoy ahora ->
        block_index = 1
        while block_index < len(chain):
            # comprueblo que el bloque actual cumple la ecuacion programada ->
            current_block = chain[block_index]
            # 1. el previous hash del bloque actuak, tiene que coincidir con el hash del bloque anterior.
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            
            # consulto la prueba del bloue previo ->
            previous_proof = previous_block['proof']
            # cpnsulto el valor de la prueba actual ->
            proof = current_block['proof']
            
            ecuacion = (proof**2 - previous_proof**2)
            hash_operation = hashlib.sha256(str(ecuacion).encode()).hexdigest()
            
            # si esas 4 primeras posiciones (0,1,2,3) no cumplen la proof of work ->
            if hash_operation[:4] != '0000':
                return False
            
            # seteo el bloque anterior con el valor del actual, y actualizo en 1 el indice ->
            previous_block = current_block
            block_index += 1
            
        # si la cadena es válida, devuelvo true ->
        return True
        
        
    #}

# Parte 2 - Minado de un bloque de la cadena

# primero voy a crear una web app basada en Flask ->
app = Flask(__name__)
# segundo voy a crear una BlockChain ->
blockchain = Blockchain()

