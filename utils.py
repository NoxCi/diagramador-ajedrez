def recta(p1,p2):
    m = (p2[1]-p1[1])/(p2[0]-p1[0])
    b = m*(-p1[0]) + p1[1]
    return m, (lambda x : m*x + b)
