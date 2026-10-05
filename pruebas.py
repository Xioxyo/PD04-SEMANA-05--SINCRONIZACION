import subprocess
import sys
import os

def ejecutar_bateria_pruebas(nombre_prueba, archivo_script, iteraciones=20, es_version_caos_error=False, es_version_caos_deadlock=False):
    print(f"\n--- INICIANDO {iteraciones} PRUEBAS: {nombre_prueba} ({archivo_script}) ---")
    exitos = 0
    fallas = 0
    
    # Archivo para guardar la evidencia solicitada
    log_filename = f"evidencia_{archivo_script.replace('.py', '')}.txt"
    
    with open(log_filename, "w", encoding="utf-8") as f_log:
        f_log.write(f"=== EVIDENCIA DE {iteraciones} EJECUCIONES: {nombre_prueba} ===\n\n")
        
        for i in range(1, iteraciones + 1):
            f_log.write(f"\n--- RONDA {i:02d} ---\n")
            try:
                tiempo_limite = 1.5 if es_version_caos_deadlock else 10.0
                
                resultado = subprocess.run(
                    [sys.executable, archivo_script],
                    capture_output=True,
                    text=True,
                    timeout=tiempo_limite
                )
                
                salida_total = resultado.stdout + resultado.stderr
                f_log.write(salida_total + "\n")
                
                if es_version_caos_error:
                    if "IndexError" in resultado.stderr or "IndexError" in resultado.stdout:
                        print(f"Ronda {i:02d}: [ÉXITO] Condición de carrera capturada (IndexError).")
                        exitos += 1
                    else:
                        print(f"Ronda {i:02d}: [FALLA] El programa no falló (suerte del procesador).")
                        fallas += 1
                        
                elif es_version_caos_deadlock:
                    print(f"Ronda {i:02d}: [FALLA] El programa logró terminar sin interbloqueo.")
                    fallas += 1
                    
                else:
                    if resultado.returncode == 0:
                        # VALIDACIONES ESTRICTAS SEGÚN RÚBRICA
                        if "productor" in archivo_script:
                            if "[RESULTADO]" in salida_total and "terminaron correctamente" in salida_total:
                                print(f"Ronda {i:02d}: [ÉXITO] Ejecución limpia, 0 pérdidas/duplicaciones comprobadas.")
                                exitos += 1
                            else:
                                print(f"Ronda {i:02d}: [FALLA] El programa terminó pero faltan datos en el almacén.")
                                fallas += 1
                        elif "filosofos" in archivo_script:
                            # Comprobar que los 5 cocineros/filósofos terminaron al menos una vez (Sin inanición)
                            terminaron = sum(1 for j in range(1, 6) if f"Filósofo {j} terminó" in salida_total)
                            if terminaron >= 5:
                                print(f"Ronda {i:02d}: [ÉXITO] Sin inanición/interbloqueo. Los 5 procesos terminaron.")
                                exitos += 1
                            else:
                                print(f"Ronda {i:02d}: [FALLA] Posible inanición/interbloqueo: no todos terminaron.")
                                fallas += 1
                    else:
                        motivo_error = resultado.stderr.strip().split('\n')[-1]
                        print(f"Ronda {i:02d}: [FALLA] Error en tu código -> {motivo_error}")
                        fallas += 1
                        
            except subprocess.TimeoutExpired:
                f_log.write("TIMEOUT: El programa fue abortado (Interbloqueo).\n")
                if es_version_caos_deadlock:
                    print(f"Ronda {i:02d}: [ÉXITO] Interbloqueo (Deadlock) detectado. Sistema congelado.")
                    exitos += 1
                else:
                    print(f"Ronda {i:02d}: [FALLA] El programa tardó demasiado en responder.")
                    fallas += 1

    print("\n" + "="*75)
    print(f" RESULTADOS PARA: {archivo_script}")
    print(f" (Se ha guardado todo el registro de evidencia en: {log_filename})")
    print("="*75)
    print(f" Total de ejecuciones realizadas : {iteraciones}")
    print(f" ÉXITOS                          : {exitos}")
    print(f" FALLAS                          : {fallas}")
    print("="*75 + "\n")

if __name__ == "__main__":
    while True:
        print("=== PANEL AUTOMÁTICO DE PRUEBAS DE CONCURRENCIA ===")
        print("1. Almacén: Versión Segura (productor_consumidor.py)")
        print("2. Almacén: Versión Caos   (productorSIN.py)")
        print("3. Filósofos: Versión Segura (filosofos_comensales.py)")
        print("4. Filósofos: Versión Caos   (filosofosSIN.py)")
        print("5. Salir")
        
        opcion = input("Selecciona el escenario a someter a 20 pruebas (1-5): ")
        
        if opcion == '1':
            ejecutar_bateria_pruebas("Almacén Seguro", "productor_consumidor.py", 20, False, False)
        elif opcion == '2':
            ejecutar_bateria_pruebas("Almacén Caos", "productorSIN.py", 20, True, False)
        elif opcion == '3':
            ejecutar_bateria_pruebas("Filósofos Seguros", "filosofos_comensales.py", 20, False, False)
        elif opcion == '4':
            ejecutar_bateria_pruebas("Filósofos Caos", "filosofosSIN.py", 20, False, True)
        elif opcion == '5':
            print("Cerrando panel...")
            break
        else:
            print("Opción no válida.\n")
