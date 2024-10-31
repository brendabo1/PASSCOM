import requests
from collections import deque

# URLs dos servidores das companhias
SERVERS = ["http://localhost:5001", "http://localhost:5002", "http://localhost:5003"]

def get_routes_from_server(server_url, city):
    try:
        response = requests.get(f"{server_url}/routes", params={"city": city})
        if response.status_code == 200:
            return response.json().get("connections", {})
    except requests.exceptions.RequestException:
        print(f"Erro ao conectar com o servidor {server_url}")
    return {}

def search_routes(origin, destination):
    routes = []  # Lista para armazenar todas as rotas possíveis

    # Inicializa a fila de pesquisa
    queue = deque([([origin], 0)])  # Cada item: (caminho atual, índice do servidor)
    
    while queue:
        path, server_index = queue.popleft()

        # Se o último ponto do caminho atual for o destino, armazena o caminho completo
        if path[-1] == destination:
            routes.append(path)
            continue

        # Consultar o servidor atual para obter conexões a partir da última cidade no caminho
        connections = get_routes_from_server(SERVERS[server_index], path[-1])

        # Para cada cidade destino, expande a rota
        for next_city, flights in connections.items():
            # Adiciona a nova cidade ao caminho se não foi visitada
            if next_city not in path:
                for next_server_index in range(len(SERVERS)):
                    queue.append((path + [next_city], next_server_index))

    # Retorna as rotas encontradas ou uma mensagem se não houver rotas
    return routes if routes else "Nenhuma rota encontrada"


# Exemplo de uso
origin = "LEC"
destination = "PAV"
found_routes = search_routes(origin, destination)
print(f"Rotas encontradas de {origin} para {destination}:")
for route in found_routes:
    print(" -> ".join(route))

