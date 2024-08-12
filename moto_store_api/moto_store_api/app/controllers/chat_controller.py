from flask import request, jsonify
from app import app
import openai

# Configura tu clave de API para OpenAI (GPT)
openai.api_key = 'tu-clave-de-api-de-openai'

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    data = request.get_json()
    message = data.get('message')

    # Aquí puedes integrar tu sistema para que la IA entienda el contexto
    # y responda en base a la información del sistema.

    try:
        # Ejemplo de solicitud a OpenAI
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"El usuario dice: {message}\nResponder con conocimiento del sistema de gestión de motos.",
            max_tokens=150
        )

        answer = response.choices[0].text.strip()
        return jsonify({'response': answer})

    except Exception as e:
        return jsonify({'response': 'Error al procesar la solicitud.', 'error': str(e)}), 500
