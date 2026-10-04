from threading import Thread, Lock, get_ident
from time import sleep
from datetime import datetime

# Función para obtener la hora exacta
def hora_actual():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

# Creación de 5 tenedores 
tenedores = [Lock() for _ in range(5)]
print_lock = Lock()

def print_seguro(mensaje):
    with print_lock:
        print(mensaje)

def comer(i): 
    print_seguro(f"[{hora_actual()}] [Hilo: {get_ident()}] Filósofo {i+1} está comiendo...")
    sleep(0.01) 
    print_seguro(f"[{hora_actual()}] [Hilo: {get_ident()}] Filósofo {i+1} terminó de comer.")

def filosofo_caos(i): 
    # Tenedores que necesita el filósofo
    izq = i
    der = (i+1) % 5

    print_seguro(f"\n[{hora_actual()}] [Hilo: {get_ident()}] Filósofo {i+1} necesita los tenedores {izq+1} y {der+1}")

    # TODOS TOMAN EL IZQUIERDO PRIMERO (Causa el interbloqueo)
    primero = izq
    segundo = der

    # Se intenta tomar el primer tenedor
    print_seguro(f"[{hora_actual()}] [Hilo: {get_ident()}] Filósofo {i+1} espera el tenedor {primero+1}")
    tenedores[primero].acquire()
    print_seguro(f"[{hora_actual()}] [Hilo: {get_ident()}] Filósofo {i+1} tomó el tenedor {primero+1}")

    # Forzamos una pequeña pausa para asegurar que TODOS tomen el izquierdo a la vez
    sleep(0.5)

    # Se intenta tomar el segundo tenedor (AQUÍ SE QUEDARÁN ATASCADOS PARA SIEMPRE)
    print_seguro(f"[{hora_actual()}] [Hilo: {get_ident()}] Filósofo {i+1} espera el tenedor {segundo+1}")
    tenedores[segundo].acquire()
    print_seguro(f"[{hora_actual()}] [Hilo: {get_ident()}] Filósofo {i+1} tomó el tenedor {segundo+1}")

    comer(i)

    # Se liberan los tenedores
    tenedores[segundo].release()
    tenedores[primero].release()

    print_seguro(f"\n[{hora_actual()}] [Hilo: {get_ident()}] Filósofo {i+1} liberó los tenedores {primero+1} y {segundo+1}")


if __name__ == "__main__":
    print_seguro("Iniciando cena (VERSIÓN CAOS - INTERBLOQUEO SEGURO)...\n")
    hilos = []

    for i in range(5) :
        hilo = Thread(target=filosofo_caos, args=(i,))
        hilos.append(hilo)

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join() 

    # Este mensaje jamás se imprimirá debido al interbloqueo
    print_seguro("\nTodos los filósofos terminaron correctamente.")