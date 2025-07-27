import json
from datetime import datetime
from utils.helpers import limpiar_pantalla, pausar, leer_json, escribir_json
from utils.validadores import validar_texto, validar_entero, validar_flotante

def gestionar_transferencia():
    """Gestiona la transferencia (venta o préstamo) de un jugador"""
    limpiar_pantalla()
    print("=== GESTIÓN DE TRANSFERENCIAS ===")
    
    jugadores = leer_json('data/jugadores.json')
    equipos = leer_json('data/equipos.json')
    transferencias = leer_json('data/transferencias.json')
    
    if not jugadores or len(jugadores) == 0:
        print("No hay jugadores registrados.")
        pausar()
        return
    
    if len(equipos) < 2:
        print("Se necesitan al menos 2 equipos registrados para realizar transferencias.")
        pausar()
        return
    
    # Mostrar jugadores disponibles para transferencia
    print("\nJugadores disponibles para transferencia:")
    jugadores_activos = [j for j in jugadores if j['estado'] == 'Activo']
    
    if not jugadores_activos:
        print("No hay jugadores activos disponibles para transferencia.")
        pausar()
        return
    
    for jugador in jugadores_activos:
        equipo_actual = next((e for e in equipos if e['id'] == jugador['equipo_actual']), None)
        equipo_nombre = equipo_actual['nombre'] if equipo_actual else "Desconocido"
        print(f"{jugador['id']}. {jugador['nombre']} {jugador['apellido']} ({jugador['posicion']}) - {equipo_nombre}")
    
    id_jugador = validar_entero("\nID del jugador a transferir: ")
    jugador = next((j for j in jugadores if j['id'] == id_jugador), None)
    
    if not jugador:
        print("ID de jugador no válido.")
        pausar()
        return
    
    if jugador['estado'] != 'Activo':
        print("Este jugador no está activo para transferencia.")
        pausar()
        return
    
    # Mostrar equipos destino (excluyendo el actual)
    equipo_origen = next((e for e in equipos if e['id'] == jugador['equipo_actual']), None)
    
    print("\nEquipos destino disponibles:")
    for equipo in equipos:
        if equipo['id'] != jugador['equipo_actual']:
            print(f"{equipo['id']}. {equipo['nombre']} ({equipo['pais']})")
    
    id_equipo_destino = validar_entero("\nID del equipo destino: ")
    equipo_destino = next((e for e in equipos if e['id'] == id_equipo_destino), None)
    
    if not equipo_destino:
        print("ID de equipo no válido.")
        pausar()
        return
    
    if id_equipo_destino == jugador['equipo_actual']:
        print("El jugador ya pertenece a este equipo.")
        pausar()
        return
    
    # Tipo de transferencia
    print("\nTipos de transferencia:")
    print("1. Venta")
    print("2. Préstamo")
    tipo_transferencia = validar_entero("Seleccione el tipo (1-2): ")
    
    if tipo_transferencia not in [1, 2]:
        print("Opción no válida.")
        pausar()
        return
    
    tipo = "Venta" if tipo_transferencia == 1 else "Préstamo"
    monto = 0
    fecha_fin = None
    
    if tipo == "Venta":
        monto = validar_flotante("Monto de la transferencia (en millones): ")
    else:
        fecha_fin = validar_texto("Fecha de fin de préstamo (DD/MM/AAAA): ")
    
    # Registrar la transferencia
    nueva_transferencia = {
        'id': len(transferencias) + 1,
        'id_jugador': id_jugador,
        'nombre_jugador': f"{jugador['nombre']} {jugador['apellido']}",
        'equipo_origen': equipo_origen['id'],
        'nombre_equipo_origen': equipo_origen['nombre'],
        'equipo_destino': equipo_destino['id'],
        'nombre_equipo_destino': equipo_destino['nombre'],
        'tipo': tipo,
        'monto': monto,
        'fecha': datetime.now().strftime("%d/%m/%Y"),
        'fecha_fin': fecha_fin if tipo == "Préstamo" else None
    }
    
    transferencias.append(nueva_transferencia)
    escribir_json('data/transferencias.json', transferencias)
    
    # Actualizar estado del jugador
    for j in jugadores:
        if j['id'] == id_jugador:
            j['equipo_actual'] = id_equipo_destino
            if tipo == "Préstamo":
                j['estado'] = "Préstamo"
            break
    
    # Actualizar listas de jugadores en equipos
    for equipo in equipos:
        if equipo['id'] == equipo_origen['id']:
            equipo['jugadores'].remove(id_jugador)
        elif equipo['id'] == equipo_destino['id']:
            equipo['jugadores'].append(id_jugador)
    
    escribir_json('data/jugadores.json', jugadores)
    escribir_json('data/equipos.json', equipos)
    
    print(f"\nTransferencia de {jugador['nombre']} {jugador['apellido']} registrada exitosamente!")
    pausar()