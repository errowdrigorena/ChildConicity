import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.initialize_corpuses import main as initialize_corpuses
from src.corpus_manipulator import CorpusManipulator
from src.data_formatter import DataFormatter
from src.iconicity_model import IconicityModel
from src.reader import Reader
from src.word_counter import WordCounter
from src.word_dictionary_merger import WordDictionaryMerger

def main():
    """Función principal del programa"""
    # Inicializar los corpus
    print("Inicializando corpus...")
    initialize_corpuses()
    print("Corpus inicializados correctamente.")
    
    # Definir directorios de entrada y salida
    input_dir = 'Corpus_modified'
    
    # Crear instancia del Reader
    reader = Reader()
    
    # Leer todos los directorios dentro del directorio procesado
    corpus_data = reader.read_directory(input_dir)
    
    # Mostrar la estructura del diccionario anidado
    print("\nEstructura del corpus:")
    print_directory_structure(corpus_data)
    
    # Mostrar los primeros 4 metadatos de cada archivo
    print("\nPrimeros 4 metadatos de cada archivo:")
    print_metadata(corpus_data)

def print_directory_structure(data, level=0):
    """
    Imprime la estructura del directorio de forma visual.
    
    Args:
        data (dict): Diccionario con la estructura del directorio
        level (int): Nivel de indentación actual
    """
    for dir_name, content in data.items():
        # Imprimir el nombre del directorio
        print("  " * level + "📁 " + dir_name)
        
        # Si hay archivos, imprimirlos
        if 'files' in content:
            for file in content['files']:
                print("  " * (level + 1) + "📄 " + file['metadata']['file_path'])
        
        # Procesar subdirectorios
        for key, value in content.items():
            if key != 'files':
                print_directory_structure({key: value}, level + 1)

def print_metadata(data, level=0):
    """
    Imprime los metadatos más relevantes de cada archivo.
    
    Args:
        data (dict): Diccionario con la estructura del directorio
        level (int): Nivel de indentación actual
    """
    # Lista de metadatos importantes que queremos mostrar
    important_metadata = [
        'file_path',
        'child_name',
        'child_age',
        'date',
        'participants',
        'languages'
    ]
    
    for dir_name, content in data.items():
        # Si hay archivos, mostrar sus metadatos
        if 'files' in content:
            for file in content['files']:
                print(f"\nArchivo: {file['metadata']['file_path']}")
                print("Metadatos:")
                # Mostrar los metadatos importantes
                for key in important_metadata:
                    if key in file['metadata']:
                        print(f"  {key}: {file['metadata'][key]}")
        
        # Procesar subdirectorios
        for key, value in content.items():
            if key != 'files':
                print_metadata({key: value}, level + 1)

if __name__ == "__main__":
    main() 