import json
from utils.helpers import limpiar_pantalla, pausar, leer_json, escribir_json
from utils.validadores import validar_texto, validar_entero, validar_flotante

def registrar_jugador():
    """Registra un nuevo jugador en el sistema"""
    limpiar_pantalla()
    print("=== REGISTRAR NUEVO JUGADOR ===")
    
    jugadores = leer_json('data/jugadores.json')
    equipos = leer_json('data/equipos.json')
    
    if not equipos:
        print("Error: No hay equipos registrados. Registre un equipo primero.")
        pausar()
        return
    
    nuevo_jugador = {
        'id': len(jugadores) + 1,
        'nombre': validar_texto("Nombre del jugador: "),
        'apellido': validar_texto("Apellido del jugador: "),
        'fecha_nacimiento': validar_texto("Fecha de nacimiento (DD/MM/AAAA): "),
        'nacionalidad': validar_texto("Nacionalidad: "),
        'posicion': validar_texto("Posición (Delantero/Mediocampista/Defensa/Arquero): "),
        'numero_camiseta': validar_entero("Número de camiseta: "),
        'equipo_actual': None,
        'valor_mercado': validar_flotante("Valor de mercado (en millones): "),
        'estado': 'Libre'
    }
    
    print("\nEquipos disponibles:")
    for equipo in equipos:
        print(f"{equipo['id']}. {equipo['nombre']} ({equipo['pais']})")
    
    opcion = input("\n¿Desea asignar el jugador a un equipo? (s/n): ").lower()
    if opcion == 's':
        id_equipo = validar_entero("ID del equipo: ")
        equipo_encontrado = next((e for e in equipos if e['id'] == id_equipo), None)
        
        if equipo_encontrado:
            nuevo_jugador['equipo_actual'] = id_equipo
            nuevo_jugador['estado'] = 'Activo'
            
            # Agregar jugador al equipo
            for equipo in equipos:
                if equipo['id'] == id_equipo:
                    equipo['jugadores'].append(nuevo_jugador['id'])
                    break
            
            escribir_json('data/equipos.json', equipos)
            print(f"Jugador asignado al equipo {equipo_encontrado['nombre']}")
        else:
            print("ID de equipo no válido. Jugador registrado como libre.")
    
    jugadores.append(nuevo_jugador)
    escribir_json('data/jugadores.json', jugadores)
    
    print(f"\nJugador {nuevo_jugador['nombre']} {nuevo_jugador['apellido']} registrado exitosamente!")
    pausar()

def listar_jugadores():
    """Muestra todos los jugadores registrados"""
    limpiar_pantalla()
    print("=== LISTADO DE JUGADORES ===")
    
    jugadores = leer_json('data/jugadores.json')
    equipos = leer_json('data/equipos.json')
    
    if not jugadores:
        print("No hay jugadores registrados.")
    else:
        for jugador in jugadores:
            equipo_nombre = "Libre"
            if jugador['equipo_actual']:
                equipo = next((e for e in equipos if e['id'] == jugador['equipo_actual']), None)
                if equipo:
                    equipo_nombre = equipo['nombre']
            
            print(f"\nID: {jugador['id']}")
            print(f"Nombre: {jugador['nombre']} {jugador['apellido']}")
            print(f"Posición: {jugador['posicion']}")
            print(f"Equipo: {equipo_nombre}")
            print(f"Valor: ${jugador['valor_mercado']} millones")
            print(f"Estado: {jugador['estado']}")
            print("-" * 30)
    
    pausar()