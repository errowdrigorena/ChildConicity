#!/usr/bin/env python3

from brent_manipulator import BrentManipulator

def main():
    # Crear una instancia del manipulador
    manipulator = BrentManipulator()
    
    try:
        # Procesar el directorio
        manipulator.process_directory()
        print("Procesamiento completado exitosamente")
    except Exception as e:
        print(f"Error durante el procesamiento: {str(e)}")

if __name__ == "__main__":
    main() 