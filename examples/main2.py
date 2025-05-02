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
    # print_metadata(corpus_data)
    print_sampled_metadata(corpus_data)

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
    for dir_name, content in data.items():
        if 'files' in content:
            for file in content['files']:
                print("  " * level + "📄 " + file['metadata']['file_path'])
                metadata = file['metadata']
                print("  " * (level + 1) + f"Nombre: {metadata.get('child_name', 'N/A')}")
                print("  " * (level + 1) + f"Edad: {metadata.get('child_age', 'N/A')}")
                print("  " * (level + 1) + f"Participantes: {metadata.get('participants', 'N/A')}")
                print("  " * (level + 1) + f"Tipos: {metadata.get('types', 'N/A')}")
                print()
        
        for key, value in content.items():
            if key != 'files':
                print_metadata({key: value}, level + 1)
   
def print_sampled_metadata(data):
    """
    Imprime los metadatos de 4 archivos de cada corpus.
    
    Args:
        data (dict): Diccionario con la estructura del directorio
    """
    # Obtener los directorios principales
    main_dirs = ['Brent', 'NewEngland', 'Post', 'VanKleeck']
    
    for corpus in main_dirs:
        print(f"\n=== Corpus {corpus} ===")
        if corpus in data['Corpus_modified']:
            # Obtener el primer subdirectorio
            subdirs = list(data['Corpus_modified'][corpus].keys())
            if subdirs:
                first_subdir = subdirs[0]
                if 'files' in data['Corpus_modified'][corpus][first_subdir]:
                    # Mostrar los primeros 4 archivos
                    for file in data['Corpus_modified'][corpus][first_subdir]['files'][:4]:
                        print(f"\nArchivo: {file['metadata']['file_path']}")
                        print(f"Nombre del niño: {file['metadata'].get('child_name', 'N/A')}")
                        print(f"Edad: {file['metadata'].get('child_age', 'N/A')}")
                        print(f"Participantes: {file['metadata'].get('participants', 'N/A')}")
                        print(f"Tipos: {file['metadata'].get('types', 'N/A')}")
                        if file['metadata'].get('utterances'):
                            print(f"Primera expresión: {file['metadata']['utterances'][0]['text']}")
                        print("-" * 50)

if __name__ == "__main__":
    main() 