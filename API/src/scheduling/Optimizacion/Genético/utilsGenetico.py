import random
# Definimos un cromosoma como una lista de tamaño N
# donde N es el número de slots temporales disponibles
# El ID de la operación ocupará la posición del slot temporal o 'V' si no se ha asignado
# El cromosoma se codifica como una lista de enteros
# Con separadores representados por caracteres especiales, siendo 'A' el separador de quirófanos
# y 'B' el separador de días
def cromosomaAleatorio(tiempos, quirofanos, dias, actos_pendientes):
    actos = actos_pendientes.copy()
    cromosoma = []
    # Creamos un cromosoma aleatorio
    for i in range(dias):
        for j in range(quirofanos):
            T = tiempos
            while T > 0:
                if len(actos) == 0:
                    cromosoma.append('V')
                    T -= 1
                else:
                    acto = random.choice(actos)
                    intentos = 0
                    while acto.getDuracion() > T:
                        acto = random.choice(actos)
                        intentos += 1
                        if intentos > len(actos):
                            cromosoma.append('V')
                            T -= 1
                            break
                    cromosoma.append(acto.getId())
                    actos.remove(acto)
                    T -= acto.getDuracion()
            cromosoma.append('A')
        cromosoma.append('B')
    return cromosoma

# Variables globales
# Definimos la función de fitness
def evaluar(individual, tiempos, quirofanos, dias, actos_pendientes):
    if not validar(individual, tiempos, actos_pendientes):
        return (distance(individual, tiempos, actos_pendientes)),
    # Calculamos el fitness como la suma de las ponderaciones de los actos quirúrgicos
    fitness = 0
    tiempo_quirofano = 0
    huecos_vacios = 0
    # Calculamos el fitness
    for elemento in individual:
        if elemento == 'A':
            if tiempo_quirofano>0:
                huecos_vacios += tiempos/tiempo_quirofano
            else:
                huecos_vacios += tiempos
            continue
        if elemento == 'B':
            continue
        if elemento == 'V':
            tiempo_quirofano += 0
            continue
        tiempo_quirofano += actos_pendientes[elemento].getDuracion()
        fitness += actos_pendientes[elemento].getPrioridad()
    return (huecos_vacios/fitness),

# Definimos la función de validez
def validar(individual, tiempos, actos_pendientes):
    # Comprobamos que la duración de las intervenciones no supera el tiempo disponible
    tiempo_quirofano = 0
    for elemento in individual:
        if elemento == 'A' or elemento == 'B':
            tiempo_quirofano = 0
            continue
        if elemento == 'V':
            tiempo_quirofano += 0
            continue
        tiempo_quirofano += actos_pendientes[elemento].getDuracion()
        if tiempo_quirofano > (tiempos+1):
            return False
    return True

def distance(individual,tiempos,actos_pendientes):
    # Calculamos la distancia entre los actos quirúrgicos
    dist = 0
    tiempo_quirofano = 0
    for elemento in individual:
        if tipoElemento(elemento) == 'separador':
            tiempo_quirofano = 0
            continue
        if tipoElemento(elemento) == 'hueco':
            tiempo_quirofano += 0
            continue
        tiempo_quirofano += actos_pendientes[elemento].getDuracion()
        if tiempo_quirofano > (tiempos+1):
            dist += 1
    return dist

def tipoElemento(elemento):
    if elemento == 'A' or elemento == 'B':
        return 'separador'
    if elemento == 'V':
        return 'hueco'
    else:
        return 'acto'
def cruce(ind1, ind2):
    # Obtenemos una copia de los padres
    hijo1 = ind1.copy()
    hijo2 = ind2.copy()
    # Eliminamos los separadores de los padres
    padre1 = [i for i in ind1 if i!='A' and i!='B']
    padre2 = [i for i in ind2 if i!='A' and i!='B']
    # Selecccionamos dos puntos de cruces aleatorios
    punto1, punto2, punto3, punto4 = selCruce(ind1, ind2)
    # Añadimos los genes del padre 2 al hijo 1 hasta la región de cruce
    punto1, punto2, punto3, punto4 = ordenaPuntos(punto1, punto2, punto3, punto4)
    reordenaHijo(hijo1, padre2, punto1, punto2)
    # Añadimos los genes del padre 1 al hijo 2 hasta la región de cruce
    reordenaHijo(hijo2, padre1, punto3, punto4)
    return hijo1, hijo2


def reordenaHijo(hijo1, padre2, punto1, punto2):
    for i in range(len(hijo1)):
        if i < punto1 or i > punto2:
            if hijo1[i] == 'A' or hijo1[i] == 'B':
                continue
            elif len(padre2) == 0:
                break
            hijo1[i] = padre2.pop(0)


def ordenaPuntos(punto1, punto2, punto3, punto4):
    if punto1 > punto2:
        punto = punto1
        punto1 = punto2
        punto2 = punto
    if punto3 > punto4:
        punto = punto3
        punto3 = punto4
        punto4 = punto
    return punto1, punto2, punto3, punto4


def selCruce(ind1, ind2):
    punto1 = selPunto(ind1)
    punto2 = selDosPuntos(ind1, punto1)
    punto3 = selPunto(ind2)
    punto4 = selDosPuntos(ind2, punto3)
    return punto1, punto2, punto3, punto4


def selDosPuntos(ind, punto1):
    punto2 = random.randint(0, len(ind) - 1)
    while ind[punto2] == 'A' and ind[punto2] == 'B' and punto2 == punto1:
        punto2 = random.randint(0, len(ind) - 1)
    return punto2


def selPunto(ind):
    punto = random.randint(0, len(ind) - 1)
    while ind[punto] == 'A' and ind[punto] == 'B':
        punto = random.randint(0, len(ind) - 1)
    return punto


def mutacion(individual):
    # Calculamos los índices posibles de intercambio
    indices = [i for i in range(len(individual)) if individual[i] != 'A' and individual[i] != 'B']
    # Seleccionamos dos índices aleatorios
    indices = random.choices(indices, k=2)
    # Intercambiamos los valores
    individual[indices[0]], individual[indices[1]] = individual[indices[1]], individual[indices[0]]
    return individual

# Función que traduce el fenotipo de la heurística a un cromosoma
def fenotipoACromosoma(fenotipo):
    dias = len(fenotipo)
    quirofanos = len(fenotipo[0])
    cromosoma = []
    for i in range(dias):
        for j in range(quirofanos):
            for acto in fenotipo[i][j].getActos():
                cromosoma.append(acto.getId())
            cromosoma.append('A')
        cromosoma.append('B')
    return cromosoma