#!/usr/bin/env python3

import os
from brent_manipulator import BrentManipulator

def main():
    # Obtener el directorio raíz del proyecto
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Crear una instancia del manipulador con rutas relativas al directorio raíz
    manipulator = BrentManipulator(
        base_dir=os.path.join(project_root, "Brent"),
        output_dir=os.path.join(project_root, "Brent_modified")
    )
    
    try:
        # Procesar el directorio
        manipulator.process_directory()
        print("Procesamiento completado exitosamente")
    except Exception as e:
        print(f"Error durante el procesamiento: {str(e)}")

if __name__ == "__main__":
    main() 