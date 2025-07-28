"""
Autor: Jhonatan David Pinto Andrade
Fecha:27/07/2025
Descripcion: Proyecto Gestor de torneos.
"""

import os
import json
from utils.helpers import limpiar_pantalla, pausar

# Importaciones de controladores
from controllers.equipos import registrar_equipo, listar_equipos
from controllers.jugadores import (
    registrar_jugador, 
    listar_jugadores_por_equipo, 
    eliminar_jugador
)
from controllers.cuerpotecnico import (
    registrar_cuerpo_tecnico, 
    listar_cuerpo_tecnico_por_equipo, 
    eliminar_cuerpo_tecnico
)
from controllers.torneos import registrar_torneo, listar_torneos, inscribir_equipos_torneo
from controllers.partidos import registrar_partido, listar_partidos
from controllers.transferencias import gestionar_transferencia
from controllers.estadisticas import mostrar_estadisticas

def crear_archivos_json():
    """Crea los archivos JSON necesarios si no existen"""
    archivos = [
        'data/equipos.json',
        'data/jugadores.json',
        'data/cuerpotecnico.json',
        'data/torneos.json',
        'data/partidos.json',
        'data/transferencias.json',
        'data/estadisticas.json'
    ]
    
    for archivo in archivos:
        directorio = os.path.dirname(archivo)
        if not os.path.exists(directorio):
            os.makedirs(directorio)
        if not os.path.exists(archivo):
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

def menu_principal():
    """Muestra el menú principal"""
    while True:
        limpiar_pantalla()
        print("=== GESTOR DE TORNEOS DE FÚTBOL ===")
        print("1. Gestión de Equipos")
        print("2. Gestión de Jugadores")
        print("3. Gestión de Cuerpo Técnico")
        print("4. Gestión de Torneos")
        print("5. Gestión de Partidos")
        print("6. Transferencias")
        print("7. Estadísticas")
        print("0. Salir")
        
        opcion = input("\nSeleccione una categoría: ")
        
        if opcion == "1":
            menu_equipos()
        elif opcion == "2":
            menu_jugadores()
        elif opcion == "3":
            menu_cuerpo_tecnico()
        elif opcion == "4":
            menu_torneos()
        elif opcion == "5":
            menu_partidos()
        elif opcion == "6":
            gestionar_transferencia()
        elif opcion == "7":
            mostrar_estadisticas()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            pausar()

def menu_equipos():
    """Submenú para gestión de equipos"""
    while True:
        limpiar_pantalla()
        print("=== GESTIÓN DE EQUIPOS ===")
        print("1. Registrar nuevo equipo")
        print("2. Listar equipos registrados")
        print("0. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            registrar_equipo()
        elif opcion == "2":
            listar_equipos()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            pausar()

def menu_jugadores():
    """Submenú para gestión de jugadores"""
    while True:
        limpiar_pantalla()
        print("=== GESTIÓN DE JUGADORES ===")
        print("1. Registrar nuevo jugador")
        print("2. Listar jugadores por equipo")
        print("3. Eliminar jugador")
        print("0. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            registrar_jugador()
        elif opcion == "2":
            listar_jugadores_por_equipo()
        elif opcion == "3":
            eliminar_jugador()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            pausar()

def menu_cuerpo_tecnico():
    """Submenú para gestión de cuerpo técnico"""
    while True:
        limpiar_pantalla()
        print("=== GESTIÓN DE CUERPO TÉCNICO ===")
        print("1. Registrar nuevo miembro")
        print("2. Listar cuerpo técnico por equipo")
        print("3. Eliminar miembro")
        print("0. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            registrar_cuerpo_tecnico()
        elif opcion == "2":
            listar_cuerpo_tecnico_por_equipo()
        elif opcion == "3":
            eliminar_cuerpo_tecnico()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            pausar()

def menu_torneos():
    """Submenú para gestión de torneos"""
    while True:
        limpiar_pantalla()
        print("=== GESTIÓN DE TORNEOS ===")
        print("1. Registrar nuevo torneo")
        print("2. Listar torneos registrados")
        print("3. Inscribir equipos en torneo")
        print("0. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            registrar_torneo()
        elif opcion == "2":
            listar_torneos()
        elif opcion == "3":
            inscribir_equipos_torneo()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            pausar()

def menu_partidos():
    """Submenú para gestión de partidos"""
    while True:
        limpiar_pantalla()
        print("=== GESTIÓN DE PARTIDOS ===")
        print("1. Registrar nuevo partido")
        print("2. Listar partidos registrados")
        print("0. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            registrar_partido()
        elif opcion == "2":
            listar_partidos()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            pausar()

if __name__ == "__main__":
    crear_archivos_json()
    menu_principal()