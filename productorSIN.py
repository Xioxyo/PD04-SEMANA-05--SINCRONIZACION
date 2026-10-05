from threading import Thread, get_ident
from time import sleep
from datetime import datetime

buffer = []

def hora_actual(): return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def productor_caos(nombre, cantidad_datos):
    for i in range(cantidad_datos):
        dato = f"{nombre}-{i+1}"
        print(f"[{hora_actual()}] [Hilo: {get_ident()}] {nombre} colocó: {dato}")
        buffer.append(dato)
        sleep(0.1)

def consumidor_caos(nombre, cantidad_datos):
    for i in range(cantidad_datos):
        print(f"[{hora_actual()}] [Hilo: {get_ident()}] {nombre} intentando retirar...")
        dato = buffer.pop(0) # Crash seguro (IndexError)
        print(f"[{hora_actual()}] [Hilo: {get_ident()}] {nombre} retiró: {dato}")
        sleep(0.01)

if __name__ == "__main__":
    print("Iniciando simulación (VERSIÓN CAOS)...\n")
    hilos = [
        Thread(target=productor_caos, args=("ProvA", 3)),
        Thread(target=productor_caos, args=("ProvB", 3)),
        Thread(target=consumidor_caos, args=("Con1", 3)),
        Thread(target=consumidor_caos, args=("Con2", 3))
    ]
    for h in hilos: h.start()
    for h in hilos: h.join()
