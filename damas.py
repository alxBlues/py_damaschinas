import math


# Tablero inicial negras repreentadas con la letra n y blancas representadas con la letra b
# desarrollo y ajustes Equipo:
# 1. Luis Alexander Castaño Reyes, 2. Gustavo Andres Gomez Bonilla, 3. Maria Isabel Marin Henao
tablero = [['-', 'n', '-', 'n', '-', 'n', '-', 'n'],
            ['n', '-', 'n', '-', 'n', '-', 'n', '-'],
            ['-', 'n', '-', 'n', '-', 'n', '-', 'n'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['b', '-', 'b', '-', 'b', '-', 'b', '-'],
            ['-', 'b', '-', 'b', '-', 'b', '-', 'b'],
            ['b', '-', 'b', '-', 'b', '-', 'b', '-']]

letras = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
jugador = 'b'  # Siempre van a comenzar las blancas 
movimiento_valido = True


def imprimir_tablero():
    """Mostrar los valores iniciales del tablero."""
    print("\n".join([" ".join(row) for row in tablero]))
    print("\n")


def mo_valido(jugada, color_jugador):
    """Verificar Movimiento segun las reglas."""
    if len(jugada) != 4:
        return False

    # Buscar la ubicación de la jugada.
    mov_ori_row = letras[jugada[0].upper()]
    mov_ori_col = int(jugada[1]) - 1
    mov_des_row = letras[jugada[2].upper()]
    mov_des_col = int(jugada[3]) - 1

    # Verificar las posiciones no se salgan del tablero en filas y columnas
    if not (0 <= mov_ori_row < 8 and 0 <= mov_ori_col < 8):
        return False
    if not (0 <= mov_des_row < 8 and 0 <= mov_des_col < 8):
        return False

    ficha = tablero[mov_ori_row][mov_ori_col]
    destino = tablero[mov_des_row][mov_des_col]

    # Las fichas deben pertenecer al jugador
    if ficha.lower() != color_jugador:
        return False

    # Verificar que la casilla destino esté vacía
    if destino != '-':
        return False

    # Movimiento de una ficha normal
    if ficha.islower():
        # Movimiento simple (1 casilla diagonal)
        if abs(mov_des_row - mov_ori_row) == 1 and abs(mov_des_col - mov_ori_col) == 1:
            return True

        # Movimiento de captura (2 casillas diagonal)
        if abs(mov_des_row - mov_ori_row) == 2 and abs(mov_des_col - mov_ori_col) == 2:
            cap_row = (mov_ori_row + mov_des_row) // 2
            cap_col = (mov_ori_col + mov_des_col) // 2
            ficha_intermedia = tablero[cap_row][cap_col]
            if ficha_intermedia.lower() != color_jugador and ficha_intermedia != '-':
                return True

    # Movimiento de una dama
    if ficha.isupper():
        delta_row = mov_des_row - mov_ori_row
        delta_col = mov_des_col - mov_ori_col

        if abs(delta_row) == abs(delta_col):
            steps = abs(delta_row)
            for i in range(1, steps):
                inter_row = mov_ori_row + i * (1 if delta_row > 0 else -1)
                inter_col = mov_ori_col + i * (1 if delta_col > 0 else -1)
                if tablero[inter_row][inter_col] != '-':
                    return False
            return True

    return False


def mover_ficha(jugada):
    """Realiza un movimiento válido en el tablero."""
    mov_ori_row = letras[jugada[0].upper()]
    mov_ori_col = int(jugada[1]) - 1
    mov_des_row = letras[jugada[2].upper()]
    mov_des_col = int(jugada[3]) - 1

    ficha = tablero[mov_ori_row][mov_ori_col]
    tablero[mov_ori_row][mov_ori_col] = '-'
    tablero[mov_des_row][mov_des_col] = ficha

    # Si es un movimiento de captura, elimina la ficha capturada
    if abs(mov_des_row - mov_ori_row) == 2 and abs(mov_des_col - mov_ori_col) == 2:
        cap_row = (mov_ori_row + mov_des_row) // 2
        cap_col = (mov_ori_col + mov_des_col) // 2
        tablero[cap_row][cap_col] = '-'

    # Promoción a dama
    if ficha == 'b' and mov_des_row == 0:
        tablero[mov_des_row][mov_des_col] = 'B'
    elif ficha == 'n' and mov_des_row == 7:
        tablero[mov_des_row][mov_des_col] = 'N'


def comprobar_victoria():
    """Comprueba si uno de los jugadores ha ganado."""
    hay_negras = any('n' in row or 'N' in row for row in tablero)
    hay_blancas = any('b' in row or 'B' in row for row in tablero)
    return not (hay_negras and hay_blancas)


def reiniciar_juego():
    """Reinicia el tablero y las variables a su estado inicial."""
    global tablero, jugador, movimiento_valido
    tablero = [['-', 'n', '-', 'n', '-', 'n', '-', 'n'],
               ['n', '-', 'n', '-', 'n', '-', 'n', '-'],
               ['-', 'n', '-', 'n', '-', 'n', '-', 'n'],
               ['-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-'],
               ['b', '-', 'b', '-', 'b', '-', 'b', '-'],
               ['-', 'b', '-', 'b', '-', 'b', '-', 'b'],
               ['b', '-', 'b', '-', 'b', '-', 'b', '-']]
    jugador = 'b'  # Reinicia el turno inicial (blancas)
    movimiento_valido = True
    print("¡El juego se ha reiniciado!")
    imprimir_tablero()


# Inicio del juego
print("Bienvenidos al juego de Damas Chinas")
imprimir_tablero()

# Función de evaluación
def funcion_evaluacion(tablero):
    """
    Evalúa el tablero desde la perspectiva de las negras.
    """
    puntuacion = 0
    for fila in tablero:
        for ficha in fila:
            if ficha == 'n':  # Peón negro
                puntuacion += 1
            elif ficha == 'N':  # Dama negra
                puntuacion += 3
            elif ficha == 'b':  # Peón blanco
                puntuacion -= 1
            elif ficha == 'B':  # Dama blanca
                puntuacion -= 3
    return puntuacion

# Generación de movimientos legales para negras
def movimientos_legales(tablero, color_jugador):
    """
    Genera una lista de movimientos válidos para las fichas del jugador.
    Prioriza movimientos de captura sobre movimientos simples.
    """
    movimientos_captura = []
    movimientos_simples = []

    for fila in range(8):
        for col in range(8):
            if tablero[fila][col].lower() == color_jugador:
                for delta_fila, delta_col in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    nueva_fila = fila + delta_fila
                    nueva_col = col + delta_col

                    # Movimiento simple
                    if (0 <= nueva_fila < 8 and 0 <= nueva_col < 8
                            and tablero[nueva_fila][nueva_col] == '-'):
                        movimientos_simples.append(((fila, col), (nueva_fila, nueva_col)))

                    # Movimiento de captura
                    captura_fila = fila + 2 * delta_fila
                    captura_col = col + 2 * delta_col
                    intermedia_fila = fila + delta_fila
                    intermedia_col = col + delta_col

                    if (0 <= captura_fila < 8 and 0 <= captura_col < 8
                            and tablero[captura_fila][captura_col] == '-'
                            and tablero[intermedia_fila][intermedia_col].lower() not in ['-', color_jugador]):
                        movimientos_captura.append(((fila, col), (captura_fila, captura_col)))

    # Priorizar capturas
    return movimientos_captura if movimientos_captura else movimientos_simples


def turno_negras():
    """
    Calcula y realiza el mejor movimiento para las negras usando MiniMax.
    """
    print("Turno de Negras (IA)")
    _, mejor_movimiento = minimax(tablero, 3, -math.inf, math.inf, True)
    print(f"Mejor movimiento calculado: {mejor_movimiento}")

    if mejor_movimiento:
        # Obtener origen y destino del movimiento
        origen, destino = mejor_movimiento
        ori_fila, ori_col = origen
        des_fila, des_col = destino

        # Aplicar el movimiento directamente al tablero
        ficha = tablero[ori_fila][ori_col]
        tablero[ori_fila][ori_col] = '-'
        tablero[des_fila][des_col] = ficha

        # Movimiento de captura
        if abs(des_fila - ori_fila) == 2:
            cap_fila = (ori_fila + des_fila) // 2
            cap_col = (ori_col + des_col) // 2
            tablero[cap_fila][cap_col] = '-'

        # Promoción a dama
        if ficha == 'n' and des_fila == 7:
            tablero[des_fila][des_col] = 'N'

        imprimir_tablero()
    else:
        print("No hay movimientos posibles para las negras. Pierden el turno.")


def mover_ficha_simulado(tablero, movimiento):
    """
    Simula un movimiento en el tablero sin afectar el estado original.
    """
    nuevo_tablero = [fila[:] for fila in tablero]
    (origen, destino) = movimiento
    ori_fila, ori_col = origen
    des_fila, des_col = destino

    ficha = nuevo_tablero[ori_fila][ori_col]
    nuevo_tablero[ori_fila][ori_col] = '-'
    nuevo_tablero[des_fila][des_col] = ficha

    # Movimiento de captura
    if abs(des_fila - ori_fila) == 2:
        cap_fila = (ori_fila + des_fila) // 2
        cap_col = (ori_col + des_col) // 2
        nuevo_tablero[cap_fila][cap_col] = '-'

    # Promoción a dama
    if ficha == 'n' and des_fila == 7:
        nuevo_tablero[des_fila][des_col] = 'N'

    return nuevo_tablero

# Algoritmo MiniMax con poda alfa-beta
def minimax(tablero, profundidad, alfa, beta, maximizando):
    """
    Implementa el algoritmo MiniMax con poda alfa-beta.
    """
    if profundidad == 0 or comprobar_victoria():
        eval_actual = funcion_evaluacion(tablero)
        print(f"Profundidad alcanzada o victoria detectada. Evaluación: {eval_actual}")
        return eval_actual, None

    color = 'n' if maximizando else 'b'
    movimientos = movimientos_legales(tablero, color)
    print(f"Movimientos legales para {'negras' if maximizando else 'blancas'}: {movimientos}")

    if not movimientos:
        eval_actual = funcion_evaluacion(tablero)
        print(f"No hay movimientos legales. Evaluación: {eval_actual}")
        return eval_actual, None

    mejor_movimiento = None

    if maximizando:
        max_eval = -math.inf
        for movimiento in movimientos:
            nuevo_tablero = mover_ficha_simulado(tablero, movimiento)
            eval_actual, _ = minimax(nuevo_tablero, profundidad - 1, alfa, beta, False)
            print(f"Maximización: Movimiento {movimiento}, Evaluación: {eval_actual}")
            if eval_actual > max_eval:
                max_eval = eval_actual
                mejor_movimiento = movimiento
            alfa = max(alfa, eval_actual)
            if beta <= alfa:
                print("Poda en maximización")
                break
        return max_eval, mejor_movimiento
    else:
        min_eval = math.inf
        for movimiento in movimientos:
            nuevo_tablero = mover_ficha_simulado(tablero, movimiento)
            eval_actual, _ = minimax(nuevo_tablero, profundidad - 1, alfa, beta, True)
            print(f"Minimización: Movimiento {movimiento}, Evaluación: {eval_actual}")
            if eval_actual < min_eval:
                min_eval = eval_actual
                mejor_movimiento = movimiento
            beta = min(beta, eval_actual)
            if beta <= alfa:
                print("Poda en minimización")
                break
        return min_eval, mejor_movimiento

# Turno de la IA para negras
def turno_negras():
    """
    Calcula y realiza el mejor movimiento para las negras usando MiniMax.
    """
    print("Turno de Negras (IA)")
    _, mejor_movimiento = minimax(tablero, 3, -math.inf, math.inf, True)
    if mejor_movimiento:
        # Obtener origen y destino del movimiento
        origen, destino = mejor_movimiento
        ori_fila, ori_col = origen
        des_fila, des_col = destino

        # Aplicar el movimiento directamente al tablero
        ficha = tablero[ori_fila][ori_col]
        tablero[ori_fila][ori_col] = '-'
        tablero[des_fila][des_col] = ficha

        # Movimiento de captura
        if abs(des_fila - ori_fila) == 2:
            cap_fila = (ori_fila + des_fila) // 2
            cap_col = (ori_col + des_col) // 2
            tablero[cap_fila][cap_col] = '-'

        # Promoción a dama
        if ficha == 'n' and des_fila == 7:
            tablero[des_fila][des_col] = 'N'

        imprimir_tablero()
    else:
        print("No hay movimientos posibles para las negras. Pierden el turno.")

# Ajuste en el bucle principal
while movimiento_valido:
    if jugador == 'b':  # Turno del jugador
        print("Turno de Blancas (Jugador)")
        movimiento = input("Introduce tu movimiento (ejemplo: F5D3 o escribe 'reiniciar'): ").strip().upper()

        if movimiento == "REINICIAR":
            reiniciar_juego()
            continue

        if mo_valido(movimiento, jugador):
            mover_ficha(movimiento)
            imprimir_tablero()

            if comprobar_victoria():
                print("¡Ganan las Blancas!")
                break

            jugador = 'n'
        else:
            print("Movimiento no válido, inténtalo de nuevo.")
    else:  # Turno de la IA (Negras)
        turno_negras()
        if comprobar_victoria():
            print("¡Ganan las Negras!")
            break
        jugador = 'b'