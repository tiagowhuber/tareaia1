import heapq


def read_graph(file_name):
    graph = {}  # inicializamos el grafo
    with open(file_name, 'r') as file:
        for line in file:
            # si empieza con la palabra "init", lo asigno al nodo inicial
            if line.startswith('Init:'):
                init_node = line.split()[1]
            # si empieza con la palabra "goal", lo asigno al nodo objetivo
            elif line.startswith('goal:'):
                goal_node = line.split()[1]
            # si empieza con la palabra "edges" hago break para empezar a leer las aristas
            # no supe como leer las aristas sin poner una palabra (en este caso "edges") que separara la asignacion de euristicas con el peso de las aristas
            elif line.startswith('edges:'):
                break
            else:  # si no empieza con ni una palabra, asigno la heuristica al nodo
                node, heuristic = line.split()
                graph[node] = {'heuristic': int(heuristic)}
                # una vez leida la palabra "edges" hacemos break y empezamos a leer las aristas en otro ciclo for
        for line in file:
            node1, node2, cost = line.split(',')
            graph[node1][node2] = int(cost)
            graph[node2][node1] = int(cost)
    return graph, init_node, goal_node


def dfs(graph, start, goal):
    visited = set()
    # insertamos el nodo inicial al stack (el 0 es la cantidad de nodos visitados)
    stack = [(start, [start], 0)]
    while stack:  # para dfs usamos stack
        expanded = 1
        # primero hacemos pop al nodo inicial y esto nos retorna el nodo y las aristas que tiene
        node, path, cost = stack.pop()
        if node == goal:  # si el nodo que hicimos pop es el objetivo, h=retornamos el camino, el costo y la cant de veces expandido
            return path, cost, expanded
        if node not in visited:
            visited.add(node)  # agregamos el nodo entre los nodos vicitados
            for vecino in graph[node]:  # hacemos un for con los vecinos
                if vecino not in visited:  # si uno de los nodos vecinos del nodo no fue visitado, lo visitamos
                    # agregamos la arista vecina al camino
                    new_path = path + [vecino]
                    # agregamos el costo
                    new_cost = cost + graph[node][vecino]
                    # agregamos el nodo al stack
                    stack.append((vecino, new_path, new_cost))
    expanded = expanded + 1
    return None, None, None  # camino no encontrado


def ucs(graph, start, goal):
    visited = set()  # la lista visited es porque no queremos nodos repetidos
    queue = [(0, [start])]
    expanded = 0

    while queue:  # para ucs usamos queue
        (cost, path) = heapq.heappop(queue)
        node = path[-1]
        expanded = 1

        if node not in visited:
            visited.add(node)  # agregamos el nodo

            if node == goal:  # si es el objetivo, retornamos el camino, costo y la cantidad de ramas expandidas
                return path, cost, expanded

            # ya que para ucs no usamos heuristica, la borramos.
            del graph[node]['heuristic']

            for vecino, weight in graph[node].items():
                expanded = expanded + 1
                if vecino not in visited:
                    new_cost = cost + weight
                    new_path = list(path)
                    new_path.append(vecino)  # agregamos el nodo al camino
                    # agregamos al queue el siguiente nodo y agregamos su costo
                    heapq.heappush(queue, (new_cost, new_path))

    return None, None, None

# no alcance a implementar greedy y a*


# imprimimos los resultados
graph, init_node, goal_node = read_graph('graph.txt')
# print(init_node, goal_node)

print('dfs:\n')
path, cost, expanded = dfs(graph, init_node, goal_node)
print('Camino encontrado :', path)
print('Costo: ', cost)
print('Cantidad de nodos expadidos: ', expanded)

print('\nucs:\n')
path, cost, expanded = ucs(graph, init_node, goal_node)
print('Camino encontrado :', path)
print('Costo: ', cost)
print('Cantidad de nodos expadidos: ', expanded)
