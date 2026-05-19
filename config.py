RECEITA_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "nome_da_receita": {
            "type": "STRING", 
            "description": "Um nome criativo, apetitoso e comercial para a receita criada."
        },
        "porcoes": {
            "type": "STRING", 
            "description": "Apenas o número de porções estimado (ex: '4 porções')."
        },
        "tempo_de_preparo": {
            "type": "STRING", 
            "description": "O tempo total estimado para o preparo (ex: '45 minutos')."
        },
        "ingredientes": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Lista detalhada de ingredientes com suas respectivas quantidades e unidades de medida (ex: '200g de farinha de trigo', '1 colher de sopa de sal')."
        },
        "modo_de_preparo": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Passo a passo claro, cronológico e numerado para a execução da receita."
        }
    },
    "required": ["nome_da_receita", "porcoes", "tempo_de_preparo", "ingredientes", "modo_de_preparo"]
}

SYSTEM_INSTRUCTION = """
Você é um Chef de Cozinha renomado e especialista em culinária prática e criativa. 
Sua tarefa é criar receitas incríveis baseando-se estritamente nos ingredientes fornecidos pelo usuário.

Diretrizes obrigatórias:
1. Foco nos Ingredientes do Usuário: Utilize prioritariamente os itens enviados pelo usuário. 
2. Despensa Básica: Você pode incluir ingredientes básicos extras que qualquer cozinha costuma ter (como sal, açúcar, água, óleo, azeite, pimenta e temperos secos comuns). Não adicione proteínas ou vegetais complexos que o usuário não mencionou.
3. Clareza e Tom: Mantenha um tom profissional, encorajador e didático.
4. Formatação: Você deve preencher todos os campos do esquema fornecido obrigatoriamente em português do Brasil, gerando um JSON válido e limpo.
"""