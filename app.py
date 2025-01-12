from flask import Flask, request, jsonify,render_template
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/check-symptoms', methods=['POST'])
def check_symptoms():
    data = request.json
    symptoms = data.get('symptoms', [])
    duration = data.get('duration', '')
    ageGroup = data.get('ageGroup', '')
    adviceType = data.get('adviceType', [])
    detailedSymptoms = data.get('detailedSymptoms', '')

    if not symptoms:
        return jsonify({"error": "Molimo izaberite simptome"}), 400

    prompt = (
        f"Ti si medicinski asistent. Korisnik ima sledeće simptome: {', '.join(symptoms)}. "
        f"Simptomi traju {duration}. Korisnik pripada starosnoj grupi: {ageGroup}. "
        f"Dodatni opis simptoma: {detailedSymptoms}. "
        f"Korisnik želi savete o sledećem: {', '.join(adviceType)}."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ti si stručnjak za medicinu. Odgovaraj na crnogorskom jeziku."},
                {"role": "user", "content": prompt}
            ]
        )
        advice = response['choices'][0]['message']['content']
        return jsonify({"advice": advice}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port, debug=True)
