from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Carregar dados de voos da companhia a partir de um arquivo JSON local
def load_flight_data():
    with open("routes.json", "r") as file:
        return json.load(file)

flight_data = load_flight_data()

@app.route('/routes', methods=['GET'])
def get_routes():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "Cidade não especificada"}), 400

    # Retorna as conexões a partir da cidade solicitada
    connections = flight_data.get(city, {})
    return jsonify({"connections": connections})

if __name__ == '__main__':
    app.run(port=5000)  # Alterar a porta para cada servidor diferente
