from threading import Thread, get_ident, Lock
from time import sleep
from datetime import datetime

# Estructura del buffer compartida (SIN SEMÁFOROS)
buffer = []

# Candado exclusivo para que la consola no mezcle textos
print_lock = Lock()

def hora_actual():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def print_seguro(mensaje):
    with print_lock:
        print(mensaje)

def productor_caos(nombre, cantidad_datos):
    for i in range(cantidad_datos):
        dato = i + 1
        
        print_seguro(f"[{hora_actual()}] [Hilo: {get_ident()}] {nombre} listo para colocar dato...")
        
        # Acceso directo al buffer sin Mutex
        buffer.append(dato)
        print_seguro(f"[{hora_actual()}] [Hilo: {get_ident()}] {nombre} colocó dato: {dato} | Buffer actual: {buffer}")
        
        sleep(0.3)

def consumidor_caos(nombre, cantidad_datos):
    for i in range(cantidad_datos):
        print_seguro(f"[{hora_actual()}] [Hilo: {get_ident()}] {nombre} intentando retirar dato...")
        
        # AQUÍ CRASHEARÁ: Intentará hacer pop(0) de una lista vacía.
        dato = buffer.pop(0) 
        print_seguro(f"[{hora_actual()}] [Hilo: {get_ident()}] {nombre} retira dato: {dato} | Buffer actual: {buffer}")
        
        sleep(0.01)


if __name__ == "__main__":
    print_seguro("Iniciando simulación (VERSIÓN CAOS - CONDICIÓN DE CARRERA)...\n")
    hilos = []
    
    # Se crean 2 productores y 2 consumidores concurrentes
    hilos.append(Thread(target=productor_caos, args=("Productor A", 3)))
    hilos.append(Thread(target=productor_caos, args=("Productor B", 3)))
    hilos.append(Thread(target=consumidor_caos, args=("Consumidor 1", 3)))
    hilos.append(Thread(target=consumidor_caos, args=("Consumidor 2", 3)))

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join() 

    print_seguro("\nSimulación finalizada (este mensaje se imprime aunque los consumidores hayan muerto).")