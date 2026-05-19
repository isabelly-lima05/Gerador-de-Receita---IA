import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import RECEITA_SCHEMA, SYSTEM_INSTRUCTION

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)

# 1. LISTA LOCAL DE PALAVRAS PROIBIDAS (Adicione ou remova conforme necessário)
PALAVRAS_PROIBIDAS = [
    "veneno", "bomba", "droga", "tóxico", "pedra", "plastico", "vidro", 
    "metal", "arma", "faca", "sangue", "morrer", "morte", "suicidio",
    "acido", "gasolina", "diesel", "detergente", "sabao", "bateria"
]

def generate_recipe(ingredientes):
    lista_ingredientes = ", ".join(ingredientes)
    conteudo_prompt = f"Crie uma receita utilizando estes ingredientes: {lista_ingredientes}."
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conteudo_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=RECEITA_SCHEMA,
        )
    )
    return response.text

@app.route("/")
def root():
    return jsonify({
        "status": "success",
        "message": "API Gerador de Receitas funcionando!",
        "version": "1.1"
    }), 200

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    
    if not data or "ingredientes" not in data:
        return jsonify({
            "status": "error",
            "message": "Por favor, envie uma lista de ingredientes no formato JSON."
        }), 400
        
    ingredientes = data.get("ingredientes", [])
    
    if not isinstance(ingredientes, list) or len(ingredientes) < 3:
        return jsonify({
            "status": "error",
            "message": "Você precisa fornecer no mínimo 3 ingredientes."
        }), 400
    
    # Camada de Proteção 1: Validação de texto local contra palavras pesadas/inanimadas
    for ingrediente in ingredientes:
        texto_ingrediente = str(ingrediente).lower()
        if any(palavra in texto_ingrediente for  palavra in PALAVRAS_PROIBIDAS):
            return jsonify({
                "status": "error",
                "message": "Tente Novamente. Isso fere nossas Politicas de Diretrizes"
            }), 400
            
    try:
        receita_json_string = generate_recipe(ingredientes)
        receita_estruturada = json.loads(receita_json_string)
        
        # Camada de Proteção 2: O Gemini detectou violação profunda que passou pelo filtro local
        if receita_estruturada.get("violacao_diretriz") is True:
            return jsonify({
                "status": "error",
                "message": "Tente Novamente. Isso fere nossas Politicas de Diretrizes"
            }), 400
            
        # Remove a flag de controle interna antes de enviar a resposta ao usuário final
        receita_estruturada.pop("violacao_diretriz", None)
        
        return jsonify({
            "status": "success",
            "ingredientes_enviados": ingredientes,
            "dados_receita": receita_estruturada
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao gerar a receita: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)