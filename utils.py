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
