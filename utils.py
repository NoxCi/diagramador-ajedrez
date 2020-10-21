def recta(p1,p2):
    """
    Modela una linea recta, devuelve su pendiente y la funcion
    que modela la recta.
    """
    m = (p2[1]-p1[1])/(p2[0]-p1[0])
    b = m*(-p1[0]) + p1[1]
    return m, (lambda x : m*x + b)

def is_number(n):
    """
    Checa si un string es un numero, si lo es regresa el numero
    de lo contrario regresa False
    """
    try:
        return int(n)
    except Exception as e:
        return False

def chess_position(col, row):
    """
    Covierte una posicion capaz de axceder a un arreglo de 8x8
    a un formato de ajedrez
    """
    letras='abcdefgh'
    casilla = letras[col] + str(8-row)
    return casilla

def chess_directions(piece,color,col,row):
    """
    Devuelve las posibles direcciones de una pieza
    """
    recursive = False
    if piece == 'P':
        if color == 'n':
            directions = [(0,1),(-1,1),
            (1,1),]
            if row == 1:
                directions.append((0,2))
        if color == 'b':
            directions = [(0,-1),(-1,-1),
            (1,-1),]
            if row == 6:
                directions.append((0,-2))
    if piece == 'R':
        directions = [(0,1),(-1,1),
        (1,1),(0,-1),(-1,-1),
        (1,-1),(-1,0),(1,0)]
        if col == 4 and row == 7 and color == 'b':
            directions.append((2,0))
            directions.append((-2,0))
        if col == 4 and row == 0 and color == 'n':
            directions.append((2,0))
            directions.append((-2,0))
    if piece == 'D':
        recursive = True
        directions = [(0,1),(-1,1),
        (1,1),(0,-1),(-1,-1),
        (1,-1),(-1,0),(1,0)]
    if piece == 'T':
        recursive=True
        directions = [(0,1),(0,-1),
        (-1,0),(1,0)]
    if piece == 'A':
        recursive = True
        directions = [(1,1), (-1,1),
        (-1,-1), (1,-1)]
    if piece == 'C':
        directions=[(1,-2),(-1,-2),
        (2,1),(2,-1),(1,2),
        (-1,2),(-2,1),(-2,-1)]

    return directions, recursive
