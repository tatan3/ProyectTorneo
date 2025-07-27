import os
import platform
import json

def limpiar_pantalla():
    """Limpia la pantalla de la consola según el sistema operativo"""
    sistema = platform.system()
    if sistema == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input("\nPresione Enter para continuar...")

def leer_json(ruta):
    """Lee un archivo JSON y retorna su contenido"""
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def escribir_json(ruta, datos):
    """Escribe datos en un archivo JSON"""
    with open(ruta, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)