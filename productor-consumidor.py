from threading import Thread, Semaphore, get_ident
from datetime import datetime

# Estructura del almacén que se comparte
CAPACIDAD = 5
almacen = []

# Los semáforos
mutex = Semaphore(1)
vacios = Semaphore(CAPACIDAD)
llenos = Semaphore(0)

def hora_actual():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def proveedor(nombre, cantidad_insumos):
    for i in range(cantidad_insumos):
        insumo = i + 1
        
        vacios.acquire()
        mutex.acquire()
        almacen.append(insumo)
        print(f"[{hora_actual()}] [Hilo: {get_ident()}] {nombre} produjo insumo: {insumo}")
        mutex.release()
        llenos.release()

def cocinero(nombre, cantidad_insumos):
    for i in range(cantidad_insumos):
        llenos.acquire()
        mutex.acquire()
        insumo = almacen.pop(0)
        print(f"[{hora_actual()}] [Hilo: {get_ident()}] {nombre} consumió insumo: {insumo}")
        mutex.release()
        vacios.release()
