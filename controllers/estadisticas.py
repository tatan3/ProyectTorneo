import json
from utils.helpers import limpiar_pantalla, pausar, leer_json
from utils.validadores import validar_entero

def mostrar_estadisticas():
    """Muestra estadísticas de torneos y equipos"""
    limpiar_pantalla()
    print("=== ESTADÍSTICAS ===")
    
    estadisticas = leer_json('data/estadisticas.json')
    equipos = leer_json('data/equipos.json')
    
    if not estadisticas:
        print("No hay estadísticas registradas.")
        pausar()
        return
    
    print("\nEstadísticas disponibles:")
    for i, estadistica in enumerate(estadisticas, 1):
        equipo = next((e for e in equipos if e['id'] == estadistica['id_equipo']), None)
        nombre_equipo = equipo['nombre'] if equipo else "Equipo desconocido"
        print(f"{i}. {nombre_equipo} - {estadistica['torneo']}")
    
    opcion = validar_entero("\nSeleccione estadística a ver (0 para todas): ")
    
    if opcion == 0:
        limpiar_pantalla()
        print("=== TODAS LAS ESTADÍSTICAS ===")
        for estadistica in estadisticas:
            equipo = next((e for e in equipos if e['id'] == estadistica['id_equipo']), None)
            nombre_equipo = equipo['nombre'] if equipo else "Equipo desconocido"
            
            print(f"\nEquipo: {nombre_equipo}")
            print(f"Torneo: {estadistica['torneo']}")
            print(f"Partidos jugados: {estadistica['pj']}")
            print(f"Partidos ganados: {estadistica['pg']}")
            print(f"Partidos empatados: {estadistica['pe']}")
            print(f"Partidos perdidos: {estadistica['pp']}")
            print(f"Goles a favor: {estadistica['gf']}")
            print(f"Goles en contra: {estadistica['gc']}")
            print(f"Diferencia de gol: {estadistica['dg']}")
            print(f"Puntos: {estadistica['puntos']}")
            print("-" * 40)
    elif 1 <= opcion <= len(estadisticas):
        estadistica = estadisticas[opcion - 1]
        equipo = next((e for e in equipos if e['id'] == estadistica['id_equipo']), None)
        nombre_equipo = equipo['nombre'] if equipo else "Equipo desconocido"
        
        limpiar_pantalla()
        print(f"=== ESTADÍSTICAS DETALLADAS ===")
        print(f"Equipo: {nombre_equipo}")
        print(f"Torneo: {estadistica['torneo']}")
        print("\nResumen:")
        print(f"Partidos jugados: {estadistica['pj']}")
        print(f"Partidos ganados: {estadistica['pg']} ({estadistica['pg']/estadistica['pj']*100:.1f}%)")
        print(f"Partidos empatados: {estadistica['pe']} ({estadistica['pe']/estadistica['pj']*100:.1f}%)")
        print(f"Partidos perdidos: {estadistica['pp']} ({estadistica['pp']/estadistica['pj']*100:.1f}%)")
        print(f"Goles a favor: {estadistica['gf']} ({estadistica['gf']/estadistica['pj']:.1f} por partido)")
        print(f"Goles en contra: {estadistica['gc']} ({estadistica['gc']/estadistica['pj']:.1f} por partido)")
        print(f"Diferencia de gol: {estadistica['dg']}")
        print(f"Puntos: {estadistica['puntos']} ({estadistica['puntos']/(estadistica['pj']*3)*100:.1f}% de puntos posibles)")
    else:
        print("Opción no válida.")
    
    pausar()