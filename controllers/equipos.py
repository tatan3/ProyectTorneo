from utils.helpers import limpiar_pantalla, pausar, leer_json, escribir_json
from utils.validadores import validar_texto, validar_entero
import json

def registrar_equipo():
    """Registra un nuevo equipo en el sistema"""
    limpiar_pantalla()
    print("=== REGISTRAR NUEVO EQUIPO ===")
    
    equipos = leer_json('data/equipos.json')
    
    nuevo_equipo = {
        'id': len(equipos) + 1,
        'nombre': validar_texto("Nombre del equipo: "),
        'fundacion': validar_entero("Año de fundación: "),
        'estadio': validar_texto("Nombre del estadio: "),
        'jugadores': [],
        'cuerpo_tecnico': []
    }
    
    equipos.append(nuevo_equipo)
    escribir_json('data/equipos.json', equipos)
    
    print(f"\nEquipo {nuevo_equipo['nombre']} registrado exitosamente!")
    pausar()

def listar_equipos():
    """Muestra todos los equipos registrados"""
    limpiar_pantalla()
    print("=== LISTADO DE EQUIPOS ===")
    
    equipos = leer_json('data/equipos.json')
    
    if not equipos:
        print("No hay equipos registrados.")
    else:
        for equipo in equipos:
            print(f"\nID: {equipo['id']}")
            print(f"Nombre: {equipo['nombre']}")
            print(f"Año fundación: {equipo['fundacion']}")
            print(f"Estadio: {equipo['estadio']}")
            print(f"Jugadores: {len(equipo['jugadores'])}")
            print(f"Cuerpo técnico: {len(equipo['cuerpo_tecnico'])}")
            print("-" * 30)
    
    pausar()