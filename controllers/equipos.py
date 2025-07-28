from utils.helpers import limpiar_pantalla, pausar, leer_json, escribir_json
from utils.validadores import validar_texto, validar_entero
import json

def registrar_equipo():
    """Registra un nuevo equipo en el sistema"""
    limpiar_pantalla()
    print("=== REGISTRAR NUEVO EQUIPO ===")
    
    equipos = leer_json('data/equipos.json')
    
    nuevo_equipo = {
        'id': max([e['id'] for e in equipos], default=0) + 1,
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

def eliminar_equipo_en_torneo():
    """Elimina un equipo registrado en un torneo"""
    limpiar_pantalla()
    print("=== ELIMINAR EQUIPO EN TORNEO ===")
    
    torneos = leer_json('data/torneos.json')
    equipos = leer_json('data/equipos.json')
    
    if not torneos:
        print("No hay torneos registrados.")
        pausar()
        return
    
    print("\nTorneos disponibles:")
    for torneo in torneos:
        print(f"{torneo['id']}. {torneo['nombre']}")
    
    id_torneo = validar_entero("\nSeleccione ID del torneo: ")
    torneo = next((t for t in torneos if t['id'] == id_torneo), None)
    
    if not torneo or not torneo['equipos_inscritos']:
        print("Torneo no válido o sin equipos inscritos.")
        pausar()
        return
    
    print("\nEquipos inscritos en este torneo:")
    equipos_torneo = [e for e in equipos if e['id'] in torneo['equipos_inscritos']]
    for equipo in equipos_torneo:
        print(f"{equipo['id']}. {equipo['nombre']}")
    
    id_equipo = validar_entero("\nSeleccione ID del equipo a eliminar: ")
    
    if id_equipo not in torneo['equipos_inscritos']:
        print("Este equipo no está inscrito en el torneo seleccionado.")
        pausar()
        return
    
    # Eliminar equipo del torneo
    torneo['equipos_inscritos'].remove(id_equipo)
    escribir_json('data/torneos.json', torneos)
    
    print("\nEquipo eliminado del torneo exitosamente!")
    pausar()

def eliminar_equipo_no_inscrito():
    """Elimina un equipo no registrado en torneos"""
    limpiar_pantalla()
    print("=== ELIMINAR EQUIPO NO INSCRITO ===")
    
    torneos = leer_json('data/torneos.json')
    equipos = leer_json('data/equipos.json')
    
    if not equipos:
        print("No hay equipos registrados.")
        pausar()
        return
    
    # Obtener equipos no inscritos en torneos
    equipos_en_torneos = set()
    for torneo in torneos:
        equipos_en_torneos.update(torneo['equipos_inscritos'])
    
    equipos_no_inscritos = [e for e in equipos if e['id'] not in equipos_en_torneos]
    
    if not equipos_no_inscritos:
        print("Todos los equipos están inscritos en torneos.")
        pausar()
        return
    
    print("\nEquipos no inscritos en torneos:")
    for equipo in equipos_no_inscritos:
        print(f"{equipo['id']}. {equipo['nombre']}")
    
    id_equipo = validar_entero("\nSeleccione ID del equipo a eliminar: ")
    equipo = next((e for e in equipos_no_inscritos if e['id'] == id_equipo), None)
    
    if not equipo:
        print("ID de equipo no válido o equipo está en torneo.")
        pausar()
        return
    
    # Eliminar completamente el equipo
    equipos = [e for e in equipos if e['id'] != id_equipo]
    escribir_json('data/equipos.json', equipos)
    
    print("\nEquipo eliminado completamente del sistema!")
    pausar()

def menu_eliminar_equipos():
    """Submenú para eliminación de equipos"""
    while True:
        limpiar_pantalla()
        print("=== ELIMINAR EQUIPOS ===")
        print("1. Eliminar equipo de un torneo")
        print("2. Eliminar equipo no inscrito")
        print("3. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            eliminar_equipo_en_torneo()
        elif opcion == "2":
            eliminar_equipo_no_inscrito()
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            pausar()