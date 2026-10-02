from threading import Semaphore, get_ident
from time import sleep
from datetime import datetime

# Estructura del almacén compartida
CAPACIDAD = 5
almacen = []

# Semáforos de sincronización
mutex = Semaphore(1)
vacios = Semaphore(CAPACIDAD)
llenos = Semaphore(0)


def hora_actual():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def proveedor(nombre, cantidad_insumos):
    # Productor
    for i in range(cantidad_insumos):
        insumo = i + 1

        # Indicar que está esperando espacio disponible
        print(f"[{hora_actual()}] [Hilo: {get_ident()}] {nombre} esperando por espacio libre...")
        
        # Si el almacén está lleno, el hilo se bloquea aquí
        vacios.acquire()

        # Acceso al almacén
        mutex.acquire()
        almacen.append(insumo)
        print(f"[{hora_actual()}] [Hilo: {get_ident()}] {nombre} colocó insumo: {insumo} ")
        mutex.release()

        # Avisar que hay un insumo disponible
        llenos.release()

        sleep(0.1)


def cocinero(nombre, cantidad_insumos):
    # Consumidor
    for i in range(cantidad_insumos):

        # Indicar que está esperando un insumo
        print(f"[{hora_actual()}] [Hilo: {get_ident()}] {nombre} esperando por insumo disponible...")

        # Si el almacén está vacío, el hilo se bloquea aquí
        llenos.acquire()

        # Acceso al almacén
        mutex.acquire()
        insumo = almacen.pop(0)
        print(f"[{hora_actual()}] [Hilo: {get_ident()}] {nombre} retira insumo: {insumo} ")
        mutex.release()

        # Avisar que hay un espacio disponible
        vacios.release()

        sleep(0.2)
