from threading import Thread, Lock, get_ident
from time import sleep
from datetime import datetime

def hora_actual(): return datetime.now().strftime("%H:%M:%S.%f")[:-3]
tenedores = [Lock() for _ in range(5)]

def comer(i): 
    print(f"[{hora_actual()}] [Hilo: {get_ident()}] Filósofo {i+1} está comiendo...")
    sleep(0.01) 

def filosofo_caos(i): 
    izq = i
    der = (i+1) % 5

    print(f"[{hora_actual()}] [Hilo: {get_ident()}] Filósofo {i+1} espera tenedor {izq+1}")
    tenedores[izq].acquire() # TODOS TOMAN EL IZQUIERDO PRIMERO
    
    sleep(0.5) # Pausa forzada para asegurar el deadlock

    print(f"[{hora_actual()}] [Hilo: {get_ident()}] Filósofo {i+1} espera tenedor {der+1}")
    tenedores[der].acquire() # ATASCADOS PARA SIEMPRE

    comer(i)

    tenedores[der].release()
    tenedores[izq].release()

if __name__ == "__main__":
    print("Iniciando cena (VERSIÓN CAOS)...\n")
    hilos = [Thread(target=filosofo_caos, args=(i,)) for i in range(5)]
    for h in hilos: h.start()
    for h in hilos: h.join()
