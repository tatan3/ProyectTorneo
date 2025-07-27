from utils.helpers import limpiar_pantalla, pausar, leer_json, escribir_json
from utils.validadores import validar_texto, validar_entero
import json

def registrar_cuerpo_tecnico():
    """Registra un nuevo miembro del cuerpo técnico"""
    limpiar_pantalla()
    print("=== REGISTRAR CUERPO TÉCNICO ===")
    
    cuerpos_tecnicos = leer_json('data/cuerpotecnico.json')
    equipos = leer_json('data/equipos.json')
    
    if not equipos:
        print("No hay equipos registrados. Registre un equipo primero.")
        pausar()
        return
    
    print("\nEquipos disponibles:")
    for equipo in equipos:
        print(f"{equipo['id']}. {equipo['nombre']}")
    
    id_equipo = validar_entero("\nID del equipo: ")
    equipo = next((e for e in equipos if e['id'] == id_equipo), None)
    
    if not equipo:
        print("ID de equipo no válido.")
        pausar()
        return
    
    nuevo_miembro = {
        'id': len(cuerpos_tecnicos) + 1,
        'nombre': validar_texto("Nombre: "),
        'apellido': validar_texto("Apellido: "),
        'rol': validar_texto("Rol (Entrenador/Asistente/Preparador físico/Médico): "),
        'nacionalidad': validar_texto("Nacionalidad: "),
        'fecha_nacimiento': validar_texto("Fecha de nacimiento (DD/MM/AAAA): "),
        'id_equipo': id_equipo
    }
    
    cuerpos_tecnicos.append(nuevo_miembro)
    escribir_json('data/cuerpotecnico.json', cuerpos_tecnicos)
    
    # Agregar al equipo
    for eq in equipos:
        if eq['id'] == id_equipo:
            eq['cuerpo_tecnico'].append(nuevo_miembro['id'])
            break
    
    escribir_json('data/equipos.json', equipos)
    
    print(f"\n{nuevo_miembro['rol']} {nuevo_miembro['nombre']} {nuevo_miembro['apellido']} registrado exitosamente!")
    pausar()

def listar_cuerpo_tecnico():
    """Muestra todos los miembros del cuerpo técnico"""
    limpiar_pantalla()
    print("=== LISTADO DE CUERPO TÉCNICO ===")
    
    cuerpos_tecnicos = leer_json('data/cuerpotecnico.json')
    equipos = leer_json('data/equipos.json')
    
    if not cuerpos_tecnicos:
        print("No hay miembros del cuerpo técnico registrados.")
    else:
        for miembro in cuerpos_tecnicos:
            equipo = next((e for e in equipos if e['id'] == miembro['id_equipo']), None)
            nombre_equipo = equipo['nombre'] if equipo else "Sin equipo"
            
            print(f"\nID: {miembro['id']}")
            print(f"Nombre: {miembro['nombre']} {miembro['apellido']}")
            print(f"Rol: {miembro['rol']}")
            print(f"Equipo: {nombre_equipo}")
            print(f"Nacionalidad: {miembro['nacionalidad']}")
            print("-" * 30)
    
    pausar()