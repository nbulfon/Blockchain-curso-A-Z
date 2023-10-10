# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 19:06:03 2023

@author: nicol
"""


# Modulo 2. Crear una criptomoneda (BulfonCoin)

#imports
# la libreria Requests (en plural) es la que voy a utilizar para verificar que todos
# los bloques de la cadena tengan la misma cantidad de nodos. Que exista un consenso.
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests as http
from uuid import uuid4
from urllib.parse import urlparse

# <region Parte 1 - Crear la cadena de bloques>
class Blockchain:
    
    #defino el constructor de la clase en python ->
    # en python, c/ metodo va con los dos puntos al final
    def __init__(self):
       #defino la cadena de bloques que voy a usar ->
       self.chain = []
       self.transactions = []
       # llamo al método, para definir al Bloque Génesis e inicializarlo ->
       # le paso el proof of work en 1, y el hash previo, que como es el B. Genesis, va en 0 ->
       self.create_block(proof = 1, previous_hash = '0')
       # creo un conjunto de nodos vacio (un conjunto en python es un listado sin orden y sin repeticion.)
       self.nodes = set()
       
    # ver que el primer argumento de cualquier funcion es self (es como el this en C#), para usar las props.
    def create_block(self, proof, previous_hash):
          #defino un diccionario que representa un bloque ->
          # indice, fecha de minado, proof of work,
          block = {
              'index' : len(self.chain)+1, 
              'timestamp' : str(datetime.datetime.now()),
              'proof' : proof,
              'previous_hash' : previous_hash,
              'transactions': self.transactions
              }
          self.transactions = []
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
            
            # consulto la prueba del bloque previo ->
            previous_proof = previous_block['proof']
            # consulto el valor de la prueba actual ->
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
    
    
    
    # función para añadir una transaccion.
    #es decir, lo que hará, es que dada la info. e/ un emisor y un receptor se intercambiarán cierto nro de monedas.
    # ¡! la lista de transaction es una lista TEMPORAL.
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append(
            {
                'sender':sender,
                'receiver':receiver,
                'amount':amount
            })
        #agarro el último de los bloques minados hasta el momento y le añado la transaccion
        previous_block = self.previous_block()
        return previous_block['index'] + 1
    
    
    def add_node(self, address):
        parsed_url =  urlparse(address)
        # doy de alta el nodo, que se está registrando a partir de la direccion asignada previamente, que viene por param.
        # los nodes son n conjunto, no un listado. Por eso tienen el metodo .add y no el .append. Porque no tienen en sí un orden establecido.
        self.nodes.add(parsed_url.netloc)
    
    # función que se llama, desde c/u de los nodos, para verificar que todos tengan la versión correcta de la chain.
    # es basicamente, la función del protocolo de consenso.
    # el nodo "ideal" para invocar a esta función, es el nodo más largo (porque a partir de él, el resto deberia "sincronizarse").
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        
        # la longitud "maxima" contra la cual comparar los nodos, es la del bloque mas largo ->
        max_length = len(self.chain)
        
        # para cada nodo, obtengo la cadena entera para sincronizar ->
        for node in network:
            response = http.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                lengthDelBloque = response.json()['length']
                chain = response.json()['chain']
                
                # si la cadena del bloque es mayor (mas larga) a la mia y encima es valida, la acepto ->
                if lengthDelBloque > max_length and self.is_chain_valid(chain):
                    max_length = lengthDelBloque
                    longest_chain = chain
                # si la cadena ha sido asignada, actualizo mi cadena para sincronizarla con la longest chain encontrada.
                # entonces, como el fundamental de la blockChain, el nodo con la cadena más larga, transmite la información
                # al resto.
                if longest_chain != None:
                    self.chain = longest_chain
                    return True
                else: return False
# </region>

# <region Parte 2 - Minado de un bloque de la cadena>

# primero voy a crear una web app basada en Flask ->
app = Flask(__name__)

# si obtengo error 500, actualizar Flash, reiniciar Spyder, y descomentar la linea de abajo ->
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# crear la dirección del nodo en el puerto estándar (5000)
node_adress = str(uuid4()).replace('-', '')

# segundo voy a crear una BlockChain ->
blockchain = Blockchain()

# Minar un nuevo bloque ->
# antes, le paso http://127.0.0.1:5000/ (localhost)
@app.route('/mine_block', methods =['GET'])

# funcion para minar un bloque.
# para minar un bloque, primero necesito resolver el problema matemático que haya.
def mine_block():
    # obtengo el ultimo bloque de la cadena ->
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    
    # llamo al metodo proof of work para empezar el proceso de minado ->
    proof = blockchain.proof_of_work(previous_proof)
    # obtengo el hash del bloque previo ->
    previous_hash = blockchain.hash(previous_block)
    
    blockchain.add_transaction(sender = node_adress, receiver = 'Nicolas Bulfón', amount = 10)
    
    block = blockchain.create_block(proof, previous_hash)
    
    # armo la response, que el usuario va a ver en la web/postman ->
    response = {
        'message' : 'Bien capo. Minaste un nuevo bloque.',
        'index' : block['index'], 
        'timestamp' : block['timestamp'],
        'proof' : block['proof'],
        'previous_hash' : block['previous_hash'],
        'transactions' : block['transactions']
        }
    return jsonify(response) , 200


# Obtener la cadena de bloques por completo.
@app.route('/get_chain', methods =['GET'])
def get_chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
        }
    return jsonify(response), 200



@app.route('/is_valid', methods =['GET'])
def is_blockchain_valid():
    
    chain = blockchain.chain
    chain_valid = blockchain.is_chain_valid(chain)
    response = {}
    if chain_valid is True:
        response = {
            'message': 'Bien crack. La Blockchain es válida.',
            'chain' : blockchain.chain,
            'length' : len(blockchain.chain)
            }
    else:
        response = {
            'message': 'Revisa el asunto...la Blockchain es invalida.',
            'chain' : blockchain.chain,
            'length' : len(blockchain.chain)
            }
    
    return jsonify(response), 200


@app.route('add_transactions', methods = ['POST'])
def add_transaction():
    ficheroJson = request.get_json()
    
    # keys necesarias para el post
    transactions_keys = ['sender','receiver','amount']
    
    # verifico si para cada key del transactions_keys , la key pertenece al ficheroJson
    if not all(key in ficheroJson for key in transactions_keys):
        return 'faltan algunos elementos de la transacción', 400
    
    # obtengo el indice del bloque de la cadena que se obtendra en el futuro, cuando este bloque sea minado
    index = blockchain.add_transaction(ficheroJson['sender'], ficheroJson['receiver'], ficheroJson['amount'])
    response = {'message': f'La transacción será añadida al bloque {index}'}
    return jsonify(response), 201

# </region>


# <region Parte 3 - Descentralizar la cadena de bloques >

# descentralizaré los nodos de los bloques, para crear una red distribuida de nodos, recreando y copiando la información,
# que luego lleguen al consenso, etc.

# ejecutar la app
app.run(host = '0.0.0.0', port= 5000)

# </region>





















# Ejecuto la app.
app.run(host = '0.0.0.0', port = 5000)
