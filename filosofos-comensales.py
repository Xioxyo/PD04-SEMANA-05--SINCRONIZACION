from threading import Thread, Lock
from time import sleep

# Creación de 5 utensilios 
utensilios = [Lock() for _ in range(5)]

def preparar_plato(i): 
    print(f"Cocinero {i+1} esta preparando el plato...")
    sleep(1) # Simula el tiempo que tarda en preparar el plato
    print(f"Cocinero {i+1} terminó de preparar el plato.")


def cocinero(i): 
    # Utensilios que necesita el cocinero
    izq = i
    der = (i+1) % 5

    print(f"\nCocinero {i+1} necesita los utensilios {izq+1} y {der+1}")

    if i == 4 :
        primero = izq
        segundo = der
    else:
        primero = der
        segundo = izq

    # Se intenta tomar el primer utensilio
    print(f"Cocinero {i+1} espera el utensilio {primero+1}")
    utensilios[primero].acquire()
    print(f"Cocinero {i+1} tomó el utensilio {primero+1}")

    # Se intenta tomar el segundo utensilio
    print(f"Cocinero {i+1} espera el utensilio {segundo+1}")
    utensilios[segundo].acquire()
    print(f"Cocinero {i+1} tomó el utensilio {segundo+1}")

    # Como ya se tienen los utensilios, entonces se comienza a cocinar 
    preparar_plato(i)

    # Se liberan los utensilios
    utensilios[segundo].release()
    utensilios[primero].release()

    print(f"\nCocinero {i+1} liberó los utensilios {primero+1} y {segundo+1}")


# Creacion de 5 hilos, uno para cada cocinero
hilos = []

for i in range(5) :
    hilo = Thread(target=cocinero, args=(i,))
    hilos.append(hilo)

# Se inician los 5 cocineros 
for hilo in hilos:
    hilo.start()

# Se espera a que todos terminen
for hilo in hilos:
    hilo.join() 

print("\nTodos los cocineros terminaron correctamente.")
