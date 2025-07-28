from utils.helpers import limpiar_pantalla, pausar, leer_json, escribir_json
import json
from utils.validadores import validar_texto, validar_entero

def obtener_equipo():
    """Muestra lista de equipos y retorna el seleccionado"""
    equipos = leer_json('data/equipos.json')
    
    if not equipos:
        print("No hay equipos registrados.")
        pausar()
        return None
    
    print("\nEquipos disponibles:")
    for equipo in equipos:
        print(f"{equipo['id']}. {equipo['nombre']}")
    
    id_equipo = validar_entero("\nSeleccione ID del equipo: ")
    return next((e for e in equipos if e['id'] == id_equipo), None)

def registrar_jugador():
    """Registra un nuevo jugador en un equipo específico"""
    limpiar_pantalla()
    print("=== REGISTRAR NUEVO JUGADOR ===")
    
    equipo = obtener_equipo()
    if not equipo:
        return
    
    jugadores = leer_json('data/jugadores.json')
    
    nuevo_jugador = {
        'id': max([j['id'] for j in jugadores], default=0) + 1,
        'nombre': validar_texto("Nombre completo del jugador: "),
        'dorsal': validar_entero("Número de dorsal: "),
        'posicion': validar_texto("Posición (Delantero/Mediocampista/Defensa/Arquero): "),
        'id_equipo': equipo['id']
    }
    
    jugadores.append(nuevo_jugador)
    escribir_json('data/jugadores.json', jugadores)
    
    # Actualizar lista de jugadores en el equipo
    equipo['jugadores'].append(nuevo_jugador['id'])
    escribir_json('data/equipos.json', leer_json('data/equipos.json'))
    
    print(f"\nJugador {nuevo_jugador['nombre']} registrado exitosamente en {equipo['nombre']}!")
    pausar()

def listar_jugadores_por_equipo():
    """Lista jugadores de un equipo específico"""
    limpiar_pantalla()
    print("=== LISTAR JUGADORES POR EQUIPO ===")
    
    equipo = obtener_equipo()
    if not equipo:
        return
    
    jugadores = leer_json('data/jugadores.json')
    jugadores_equipo = [j for j in jugadores if j['id_equipo'] == equipo['id']]
    
    limpiar_pantalla()
    print(f"=== JUGADORES DE {equipo['nombre'].upper()} ===")
    print("\nID  Dorsal  Nombre                Posición")
    print("-" * 50)
    
    for jugador in sorted(jugadores_equipo, key=lambda x: x['dorsal']):
        print(f"{jugador['id']:<3} {jugador['dorsal']:<7} {jugador['nombre']:<20} {jugador['posicion']}")
    
    pausar()

def eliminar_jugador():
    """Elimina completamente un jugador de un equipo"""
    limpiar_pantalla()
    print("=== ELIMINAR JUGADOR ===")
    
    equipo = obtener_equipo()
    if not equipo:
        return
    
    jugadores = leer_json('data/jugadores.json')
    jugadores_equipo = [j for j in jugadores if j['id_equipo'] == equipo['id']]
    
    if not jugadores_equipo:
        print("Este equipo no tiene jugadores registrados.")
        pausar()
        return
    
    print(f"\nJugadores de {equipo['nombre']}:")
    for jugador in jugadores_equipo:
        print(f"{jugador['id']}. {jugador['nombre']} (Dorsal: {jugador['dorsal']})")
    
    id_jugador = validar_entero("\nIngrese ID del jugador a eliminar: ")
    
    # Eliminar jugador
    jugadores = [j for j in jugadores if j['id'] != id_jugador]
    escribir_json('data/jugadores.json', jugadores)
    
    # Actualizar equipo
    equipos = leer_json('data/equipos.json')
    for eq in equipos:
        if eq['id'] == equipo['id'] and id_jugador in eq['jugadores']:
            eq['jugadores'].remove(id_jugador)
    
    escribir_json('data/equipos.json', equipos)
    print("\nJugador eliminado exitosamente!")
    pausar()