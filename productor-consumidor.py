from threading import Semaphore, get_ident
from time import sleep
from datetime import datetime

# estructura del almacen que se comparte
CAPACIDAD = 5
almacen = []

# los semaforos
mutex = Semaphore(1)
vacios = Semaphore(CAPACIDAD)
llenos = Semaphore(0)


def hora_actual():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def proveedor(nombre, cantidad_insumos):
// productor  
    for i in range(cantidad_insumos):

        # Esperar hasta que haya espacio disponible
        vacios.acquire()

        # Acceso al almacen
        mutex.acquire()

        almacen.append(insumo)

        print(f"[{hora_actual()}] "f"[Hilo: {get_ident()}] {nombre} coloca un insumo" )

        mutex.release()

        # Avisar que hay un insumo disponible
        llenos.release()

        sleep(0.2)


def cocinero(nombre, cantidad_insumos):
  //consumidor
    for i in range(cantidad_insumos):

        # Esperar hasta que haya un insumo disponible
        llenos.acquire()

        # Acceso al almacén
        mutex.acquire()

        insumo = almacen.pop(0)

        print( f"[{hora_actual()}] "f"[Hilo: {get_ident()}] {nombre} retira {insumo}")

        mutex.release()

        # Avisar que hay un espacio disponible
        vacios.release()

        sleep(0.2)
