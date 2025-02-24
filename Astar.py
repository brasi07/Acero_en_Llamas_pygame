import heapq

def heuristic(a, b):
    """Calcula la heurística (distancia Manhattan)"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    """Algoritmo A* con movimiento diagonal (si no hay bloqueo en esquinas)."""
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0),  # Movimientos ortogonales
                 (1, 1), (-1, -1), (1, -1), (-1, 1)]  # Movimientos diagonales
    
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Devuelve la ruta desde start hasta goal

        for dx, dy in neighbors:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if neighbor in grid and grid[neighbor] == 0:  # Verifica que no sea un muro
                # Para movimiento diagonal, ambas celdas ortogonales deben ser libres
                if abs(dx) == 1 and abs(dy) == 1:
                    if grid.get((current[0] + dx, current[1])) == 1 or grid.get((current[0], current[1] + dy)) == 1:
                        continue  # Bloqueo en la esquina

                tentative_g_score = g_score[current] + (1.414 if abs(dx) + abs(dy) == 2 else 1)  # 1.414 para diagonales
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # Si no encuentra camino, devuelve lista vacía
