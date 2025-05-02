import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.brend_manipulator import BrendManipulator
from src.reorganize_newengland import process_directory

def initialize_brent_corpus():
    """Inicializa el corpus de Brent"""
    print("\nInicializando corpus de Brent...")
    
    # Configurar rutas
    base_dir = os.path.join("Corpus", "Brent")
    output_dir = os.path.join("Corpus_modified", "Brent")
    
    # Crear el manipulador
    manipulator = BrendManipulator()
    manipulator.base_dir = base_dir
    manipulator.output_dir = output_dir
    
    # Procesar el directorio
    manipulator.process_directory()
    print("¡Corpus de Brent inicializado!")

def initialize_new_england_corpus():
    """Inicializa el corpus de NewEngland"""
    print("\nInicializando corpus de NewEngland...")
    
    # Configurar rutas
    input_dir = "Corpus"
    output_dir = "Corpus_modified"
    
    # Procesar el directorio usando la función process_directory
    process_directory(input_dir, output_dir)
    print("¡Corpus de NewEngland inicializado!")

def initialize_post_corpus():
    """Inicializa el corpus de Post"""
    print("\nInicializando corpus de Post...")
    
    # Configurar rutas
    base_dir = os.path.join("Corpus", "Post")
    output_dir = os.path.join("Corpus_modified", "Post")
    
    # Crear el manipulador
    manipulator = BrendManipulator()
    manipulator.base_dir = base_dir
    manipulator.output_dir = output_dir
    
    # Procesar el directorio
    manipulator.process_directory()
    print("¡Corpus de Post inicializado!")

def initialize_van_kleeck_corpus():
    """Inicializa el corpus de VanKleeck"""
    print("\nInicializando corpus de VanKleeck...")
    
    # Configurar rutas
    base_dir = os.path.join("Corpus", "VanKleeck")
    output_dir = os.path.join("Corpus_modified", "VanKleeck")
    
    # Crear el manipulador
    manipulator = BrendManipulator()
    manipulator.base_dir = base_dir
    manipulator.output_dir = output_dir
    
    # Procesar el directorio
    manipulator.process_directory()
    print("¡Corpus de VanKleeck inicializado!")

def main():
    """Función principal para inicializar todos los corpus"""
    print("Iniciando inicialización de corpus...")
    
    # Inicializar cada corpus
    initialize_brent_corpus()
    initialize_new_england_corpus()
    # initialize_post_corpus()
    # initialize_van_kleeck_corpus()
    
    print("\n¡Inicialización de corpus completada!")

if __name__ == "__main__":
    main() 