from utils.helpers import limpiar_pantalla, pausar, leer_json, escribir_json
from utils.validadores import validar_texto, validar_entero
from datetime import datetime
import json

def registrar_partido():
    """Registra un nuevo partido y su marcador"""
    limpiar_pantalla()
    print("=== REGISTRAR PARTIDO ===")
    
    torneos = leer_json('data/torneos.json')
    equipos = leer_json('data/equipos.json')
    partidos = leer_json('data/partidos.json')
    estadisticas = leer_json('data/estadisticas.json')
    
    if not torneos:
        print("No hay torneos registrados.")
        pausar()
        return
    
    print("\nTorneos disponibles:")
    for torneo in torneos:
        if len(torneo['equipos_inscritos']) >= 2:
            print(f"{torneo['id']}. {torneo['nombre']} ({len(torneo['equipos_inscritos'])} equipos)")
    
    id_torneo = validar_entero("\nID del torneo: ")
    torneo = next((t for t in torneos if t['id'] == id_torneo), None)
    
    if not torneo:
        print("ID de torneo no válido.")
        pausar()
        return
    
    if len(torneo['equipos_inscritos']) < 2:
        print("El torneo no tiene suficientes equipos inscritos.")
        pausar()
        return
    
    print("\nEquipos inscritos en el torneo:")
    equipos_torneo = [e for e in equipos if e['id'] in torneo['equipos_inscritos']]
    for equipo in equipos_torneo:
        print(f"{equipo['id']}. {equipo['nombre']}")
    
    print("\nSeleccione los equipos participantes:")
    id_local = validar_entero("ID del equipo local: ")
    equipo_local = next((e for e in equipos_torneo if e['id'] == id_local), None)
    
    id_visitante = validar_entero("ID del equipo visitante: ")
    equipo_visitante = next((e for e in equipos_torneo if e['id'] == id_visitante), None)
    
    if not equipo_local or not equipo_visitante or id_local == id_visitante:
        print("IDs de equipos no válidos.")
        pausar()
        return
    
    goles_local = validar_entero("Goles del equipo local: ")
    goles_visitante = validar_entero("Goles del equipo visitante: ")
    fecha = validar_texto("Fecha del partido (DD/MM/AAAA): ")
    
    # Registrar partido
    nuevo_partido = {
        'id': len(partidos) + 1,
        'id_torneo': id_torneo,
        'equipo_local': id_local,
        'equipo_visitante': id_visitante,
        'goles_local': goles_local,
        'goles_visitante': goles_visitante,
        'fecha': fecha,
        'estado': 'Finalizado'
    }
    
    partidos.append(nuevo_partido)
    escribir_json('data/partidos.json', partidos)
    
    # Agregar partido al torneo
    for t in torneos:
        if t['id'] == id_torneo:
            t['partidos'].append(nuevo_partido['id'])
            break
    
    escribir_json('data/torneos.json', torneos)
    
    # Actualizar estadísticas
    actualizar_estadisticas(estadisticas, id_torneo, id_local, id_visitante, goles_local, goles_visitante)
    
    print("\nPartido registrado exitosamente!")
    pausar()

def listar_partidos():
    """Muestra todos los partidos registrados"""
    limpiar_pantalla()
    print("=== LISTADO DE PARTIDOS ===")
    
    partidos = leer_json('data/partidos.json')
    equipos = leer_json('data/equipos.json')
    torneos = leer_json('data/torneos.json')
    
    if not partidos:
        print("No hay partidos registrados.")
    else:
        # Ordenar partidos por fecha (más recientes primero)
        partidos_ordenados = sorted(partidos, key=lambda x: datetime.strptime(x['fecha'], '%d/%m/%Y'), reverse=True)
        
        for partido in partidos_ordenados:
            # Obtener nombres de equipos
            equipo_local = next((e for e in equipos if e['id'] == partido['equipo_local']), None)
            nombre_local = equipo_local['nombre'] if equipo_local else "Equipo desconocido"
            
            equipo_visitante = next((e for e in equipos if e['id'] == partido['equipo_visitante']), None)
            nombre_visitante = equipo_visitante['nombre'] if equipo_visitante else "Equipo desconocido"
            
            # Obtener nombre del torneo
            torneo = next((t for t in torneos if t['id'] == partido['id_torneo']), None)
            nombre_torneo = torneo['nombre'] if torneo else "Torneo desconocido"
            
            print(f"\nID: {partido['id']}")
            print(f"Torneo: {nombre_torneo}")
            print(f"Fecha: {partido['fecha']}")
            print(f"Partido: {nombre_local} {partido['goles_local']} - {partido['goles_visitante']} {nombre_visitante}")
            print(f"Estado: {partido['estado']}")
            print("-" * 50)
    
    pausar()

def actualizar_estadisticas(estadisticas, id_torneo, id_local, id_visitante, goles_local, goles_visitante):
    """Actualiza las estadísticas basadas en el resultado del partido"""
    # Buscar o crear estadísticas para los equipos en este torneo
    stats_local = next((s for s in estadisticas if s['id_torneo'] == id_torneo and s['id_equipo'] == id_local), None)
    stats_visitante = next((s for s in estadisticas if s['id_torneo'] == id_torneo and s['id_equipo'] == id_visitante), None)
    
    if not stats_local:
        stats_local = crear_nueva_estadistica(id_torneo, id_local)
        estadisticas.append(stats_local)
    
    if not stats_visitante:
        stats_visitante = crear_nueva_estadistica(id_torneo, id_visitante)
        estadisticas.append(stats_visitante)
    
    # Actualizar estadísticas local
    stats_local['pj'] += 1
    stats_local['gf'] += goles_local
    stats_local['gc'] += goles_visitante
    stats_local['dg'] = stats_local['gf'] - stats_local['gc']
    
    # Actualizar estadísticas visitante
    stats_visitante['pj'] += 1
    stats_visitante['gf'] += goles_visitante
    stats_visitante['gc'] += goles_local
    stats_visitante['dg'] = stats_visitante['gf'] - stats_visitante['gc']
    
    # Determinar resultado
    if goles_local > goles_visitante:
        stats_local['pg'] += 1
        stats_local['puntos'] += 3
        stats_visitante['pp'] += 1
    elif goles_local < goles_visitante:
        stats_visitante['pg'] += 1
        stats_visitante['puntos'] += 3
        stats_local['pp'] += 1
    else:
        stats_local['pe'] += 1
        stats_local['puntos'] += 1
        stats_visitante['pe'] += 1
        stats_visitante['puntos'] += 1
    
    escribir_json('data/estadisticas.json', estadisticas)

def crear_nueva_estadistica(id_torneo, id_equipo):
    """Crea un nuevo registro de estadísticas"""
    return {
        'id': len(leer_json('data/estadisticas.json')) + 1,
        'id_torneo': id_torneo,
        'id_equipo': id_equipo,
        'pj': 0,
        'pg': 0,
        'pe': 0,
        'pp': 0,
        'gf': 0,
        'gc': 0,
        'dg': 0,
        'puntos': 0
    }