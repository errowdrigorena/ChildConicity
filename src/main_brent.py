#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Añadir el directorio raíz del proyecto al PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.brent_manipulator import BrentManipulator

def main():
    try:
        # Obtener la ruta del directorio raíz del proyecto
        project_root = Path(__file__).parent.parent
        
        # Construir las rutas absolutas
        brent_dir = project_root / "Corpus" / "Brent"
        corpus_modified_dir = project_root / "Corpus_modified"
        
        # Crear el directorio Corpus_modified si no existe
        if not corpus_modified_dir.exists():
            corpus_modified_dir.mkdir()
        
        brent_modified_dir = corpus_modified_dir / "Brent"
        
        # Crear el manipulador y procesar el directorio
        manipulator = BrentManipulator(str(brent_dir), str(brent_modified_dir))
        manipulator.process_directory()
        print("Procesamiento completado exitosamente")
    except FileNotFoundError as e:
        print(f"Error: El directorio no existe - {str(e)}")
        sys.exit(1)
    except PermissionError as e:
        print(f"Error: Permiso denegado - {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error durante el procesamiento: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 