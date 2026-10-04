import subprocess
import sys

def ejecutar_bateria_pruebas(nombre_prueba, archivo_script, iteraciones=20, es_version_caos_error=False, es_version_caos_deadlock=False):
    print(f"\n--- INICIANDO {iteraciones} PRUEBAS: {nombre_prueba} ({archivo_script}) ---")
    exitos = 0
    fallas = 0
    
    for i in range(1, iteraciones + 1):
        try:
            # Tiempo límite: 1.5s para deadlock, 10s para ejecuciones normales
            tiempo_limite = 1.5 if es_version_caos_deadlock else 10.0
            
            resultado = subprocess.run(
                [sys.executable, archivo_script],
                capture_output=True,
                text=True,
                timeout=tiempo_limite
            )
            
            if es_version_caos_error:
                # Busca el error específico del caos ignorando el código de estado
                if "IndexError" in resultado.stderr:
                    print(f"Ronda {i:02d}: [ÉXITO] Condición de carrera capturada (IndexError).")
                    exitos += 1
                else:
                    print(f"Ronda {i:02d}: [FALLA] El programa no falló (suerte del procesador).")
                    fallas += 1
            else:
                # En versiones seguras, esperamos que termine limpio con código 0
                if resultado.returncode == 0:
                    print(f"Ronda {i:02d}: [ÉXITO] Ejecución limpia y completada.")
                    exitos += 1
                else:
                    # Capturamos la última línea del error para que sepas por qué falló
                    motivo_error = resultado.stderr.strip().split('\n')[-1]
                    print(f"Ronda {i:02d}: [FALLA] Error en tu código -> {motivo_error}")
                    fallas += 1
                    
        except subprocess.TimeoutExpired:
            if es_version_caos_deadlock:
                print(f"Ronda {i:02d}: [ÉXITO] Interbloqueo (Deadlock) detectado. El sistema se congeló.")
                exitos += 1
            else:
                print(f"Ronda {i:02d}: [FALLA] El programa tardó demasiado en responder.")
                fallas += 1

    # Resumen final con las etiquetas solicitadas
    print("\n" + "="*50)
    print(f" RESULTADOS PARA: {archivo_script}")
    print("="*50)
    print(f" Total de ejecuciones realizadas : {iteraciones}")
    print(f" ÉXITOS                          : {exitos}")
    print(f" FALLAS                          : {fallas}")
    print("="*50 + "\n")

if __name__ == "__main__":
    while True:
        print("=== PANEL AUTOMÁTICO DE PRUEBAS DE CONCURRENCIA ===")
        print("1. Almacén: Versión Segura (productor-consumidor.py)")
        print("2. Almacén: Versión Caos   (productorSIN.py)")
        print("3. Filósofos: Versión Segura (filosofos-comensales.py)")
        print("4. Filósofos: Versión Caos   (filosofosSIN.py)")
        print("5. Salir")
        
        opcion = input("Selecciona el escenario a someter a 20 pruebas (1-5): ")
        
        if opcion == '1':
            ejecutar_bateria_pruebas("Almacén Seguro", "productor-consumidor.py", 20, False, False)
        elif opcion == '2':
            ejecutar_bateria_pruebas("Almacén Caos", "productorSIN.py", 20, True, False)
        elif opcion == '3':
            ejecutar_bateria_pruebas("Filósofos Seguros", "filosofos-comensales.py", 20, False, False)
        elif opcion == '4':
            ejecutar_bateria_pruebas("Filósofos Caos", "filosofosSIN.py", 20, False, True)
        elif opcion == '5':
            print("Cerrando panel...")
            break
        else:
            print("Opción no válida.\n")