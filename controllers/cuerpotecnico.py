import json
from utils.helpers import limpiar_pantalla, pausar, leer_json, escribir_json
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

def registrar_cuerpo_tecnico():
    """Registra nuevo miembro en un equipo específico"""
    limpiar_pantalla()
    print("=== REGISTRAR CUERPO TÉCNICO ===")
    
    equipo = obtener_equipo()
    if not equipo:
        return
    
    cuerpo_tecnico = leer_json('data/cuerpotecnico.json')
    
    nuevo_miembro = {
        'id': max([c['id'] for c in cuerpo_tecnico], default=0) + 1,
        'nombre': validar_texto("Nombre completo: "),
        'cargo': validar_texto("Cargo (Entrenador/Asistente/Preparador/Médico): "),
        'id_equipo': equipo['id']
    }
    
    cuerpo_tecnico.append(nuevo_miembro)
    escribir_json('data/cuerpotecnico.json', cuerpo_tecnico)
    
    # Actualizar equipo
    equipos = leer_json('data/equipos.json')
    for eq in equipos:
        if eq['id'] == equipo['id']:
            eq['cuerpo_tecnico'].append(nuevo_miembro['id'])
    
    escribir_json('data/equipos.json', equipos)
    print(f"\n{nuevo_miembro['cargo']} {nuevo_miembro['nombre']} registrado exitosamente!")
    pausar()

def listar_cuerpo_tecnico_por_equipo():
    """Lista cuerpo técnico de un equipo específico"""
    limpiar_pantalla()
    print("=== LISTAR CUERPO TÉCNICO POR EQUIPO ===")
    
    equipo = obtener_equipo()
    if not equipo:
        return
    
    cuerpo_tecnico = leer_json('data/cuerpotecnico.json')
    tecnicos_equipo = [t for t in cuerpo_tecnico if t['id_equipo'] == equipo['id']]
    
    limpiar_pantalla()
    print(f"=== CUERPO TÉCNICO DE {equipo['nombre'].upper()} ===")
    print("\nID  Cargo                Nombre")
    print("-" * 50)
    
    for tecnico in sorted(tecnicos_equipo, key=lambda x: x['cargo']):
        print(f"{tecnico['id']:<3} {tecnico['cargo']:<20} {tecnico['nombre']}")
    
    pausar()

def eliminar_cuerpo_tecnico():
    """Elimina completamente un miembro del cuerpo técnico"""
    limpiar_pantalla()
    print("=== ELIMINAR CUERPO TÉCNICO ===")
    
    equipo = obtener_equipo()
    if not equipo:
        return
    
    cuerpo_tecnico = leer_json('data/cuerpotecnico.json')
    tecnicos_equipo = [t for t in cuerpo_tecnico if t['id_equipo'] == equipo['id']]
    
    if not tecnicos_equipo:
        print("Este equipo no tiene cuerpo técnico registrado.")
        pausar()
        return
    
    print(f"\nCuerpo técnico de {equipo['nombre']}:")
    for tecnico in tecnicos_equipo:
        print(f"{tecnico['id']}. {tecnico['nombre']} ({tecnico['cargo']})")
    
    id_miembro = validar_entero("\nIngrese ID del miembro a eliminar: ")
    
    # Eliminar miembro
    cuerpo_tecnico = [t for t in cuerpo_tecnico if t['id'] != id_miembro]
    escribir_json('data/cuerpotecnico.json', cuerpo_tecnico)
    
    # Actualizar equipo
    equipos = leer_json('data/equipos.json')
    for eq in equipos:
        if eq['id'] == equipo['id'] and id_miembro in eq['cuerpo_tecnico']:
            eq['cuerpo_tecnico'].remove(id_miembro)
    
    escribir_json('data/equipos.json', equipos)
    print("\nMiembro eliminado exitosamente!")
    pausar()