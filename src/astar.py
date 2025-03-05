import heapq
import math

def heuristica(nodo, goal):
    """Calcula la heurística euclidiana entre dos puntos."""
    return math.sqrt((nodo[0] - goal[0])**2 + (nodo[1] - goal[1])**2)

def astar(grid, start, goal):
    """Algoritmo A* con movimiento diagonal (si no hay bloqueo en esquinas)."""
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0),  # Movimientos ortogonales
                 (1, 1), (-1, -1), (1, -1), (-1, 1)]  # Movimientos diagonales
    
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristica(start, goal)}

    filas = len(grid)
    columnas = len(grid[0])

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

            # Verificar si neighbor está dentro de los límites de la matriz
            if not (0 <= neighbor[0] < columnas and 0 <= neighbor[1] < filas):
                continue

            # Verificar si neighbor es transitable (no es un muro)
            if grid[neighbor[1]][neighbor[0]] == 1 and neighbor != goal:
                continue

            # Para movimiento diagonal, ambas celdas ortogonales deben ser libres
            if abs(dx) == 1 and abs(dy) == 1:
                if not (0 <= current[0] + dx < columnas and 0 <= current[1] < filas and 
                        0 <= current[0] < columnas and 0 <= current[1] + dy < filas):
                    continue  # Evitar accesos fuera de rango
                
                if grid[current[1]][current[0] + dx] == 1 or grid[current[1] + dy][current[0]] == 1:
                    continue  # Bloqueo en la esquina

            # Costo base del movimiento
            move_cost = 1.414 if abs(dx) + abs(dy) == 2 else 1
            
            # Usamos la función de raycasting para ver si hay línea de visión
            if not raycasting(grid, neighbor, goal):
                extra_cost = 100  # Penalización por falta de visión
            else:
                extra_cost = 0
            
            tentative_g_score = g_score[current] + move_cost + extra_cost
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristica(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # Si no encuentra camino, devuelve lista vacía



def raycasting(pantalla_binaria, origen, destino):
        """
        Chequea si hay línea de visión entre 'origen' y 'destino'.
        Primero verifica que el destino esté en la misma pantalla; luego,
        utiliza el algoritmo de Bresenham para detectar obstáculos.
        """
        x0 = origen[0]
        y0 = origen[1]
        x1 = destino[0]
        y1 = destino[1]

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        x, y = x0, y0
        while True:
            if (x,y) != (x1, y1) and pantalla_binaria[y][x] == 1:
                return False
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
        return True
