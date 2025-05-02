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

def get_age_quarter(age_str):
    """
    Convierte una cadena de edad en formato YYYYMMDD a formato YYQ.
    
    Args:
        age_str (str): Edad en formato YYYYMMDD o "X years Y months Z days"
        
    Returns:
        str: Edad en formato YYQ (años y cuarto)
    """
    try:
        # Si la edad está en formato "X years Y months Z days"
        if 'years' in age_str:
            parts = age_str.split()
            years = int(parts[0])
            months = int(parts[2])
        else:
            # Si la edad está en formato YYYYMMDD
            years = int(age_str[:2])
            months = int(age_str[2:4])
        
        quarter = (months // 3) + 1
        return f"{years:02d}Y{quarter:02d}Q"
    except (ValueError, IndexError):
        return "00Y00Q"

def group_data_by_age(processed_data):
    """
    Agrupa los datos por edad del niño en cuartos de año.
    
    Args:
        processed_data (dict): Datos procesados del corpus
        
    Returns:
        dict: Datos agrupados por edad en formato YYQ
    """
    data_grouped_by_age = {}
    
    # Iterar sobre cada corpus
    for corpus_name, corpus_data in processed_data['Corpus_modified'].items():
        # Iterar sobre cada subdirectorio (niño)
        for child_name, child_data in corpus_data.items():
            if 'files' in child_data:
                # Iterar sobre cada archivo
                for file in child_data['files']:
                    age = file['metadata'].get('child_age', '')
                    if age:
                        age_quarter = get_age_quarter(age)
                        
                        # Inicializar la estructura si no existe
                        if age_quarter not in data_grouped_by_age:
                            data_grouped_by_age[age_quarter] = {
                                'children_data': {},
                                'adults_data': {},
                                'files': []
                            }
                        
                        # Añadir los datos de niños y adultos
                        data_grouped_by_age[age_quarter]['children_data'].update(file['children_data'])
                        data_grouped_by_age[age_quarter]['adults_data'].update(file['adults_data'])
                        
                        # Obtener una frase de ejemplo de niño y adulto
                        child_example = next(iter(file['children_data'].values()))['text'] if file['children_data'] else "No hay expresiones de niños"
                        adult_example = next(iter(file['adults_data'].values()))['text'] if file['adults_data'] else "No hay expresiones de adultos"
                        
                        # Añadir información del archivo
                        data_grouped_by_age[age_quarter]['files'].append({
                            'file_path': file['metadata']['file_path'],
                            'child_name': file['metadata'].get('child_name', 'N/A'),
                            'child_age': age,
                            'age_group': age_quarter,
                            'child_example': child_example,
                            'adult_example': adult_example
                        })
    
    return data_grouped_by_age

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
    print_sampled_metadata(corpus_data)
    
    # Procesar los datos usando DataFormatter
    print("\nProcesando datos con DataFormatter...")
    processed_data = process_data_with_formatter(corpus_data)
    
    # Agrupar datos por edad
    print("\nAgrupando datos por edad...")
    data_grouped_by_age = group_data_by_age(processed_data)
    
    # Mostrar estadísticas por grupo de edad
    print("\nEstadísticas por grupo de edad:")
    for age_group, data in sorted(data_grouped_by_age.items()):
        children_count = len(data['children_data'])
        adults_count = len(data['adults_data'])
        files_count = len(data['files'])
        print(f"\nGrupo de edad {age_group}:")
        print(f"  Archivos: {files_count}")
        print(f"  Expresiones de niños: {children_count}")
        print(f"  Expresiones de adultos: {adults_count}")
        print("  Archivos incluidos:")
        for file in data['files']:
            print(f"\n    - {file['child_name']} ({file['child_age']})")
            print(f"      Grupo de edad: {file['age_group']}")
            print(f"      Archivo: {file['file_path']}")
            print(f"      Ejemplo de expresión del niño: {file['child_example']}")
            print(f"      Ejemplo de expresión del adulto: {file['adult_example']}")
            print("      " + "-" * 50)
    
    # # Crear el modelo de iconicidad
    # print("\nCreando modelo de iconicidad...")
    # formatter = DataFormatter()
    # csv_data = formatter.format_csv_data_from('iconicity_ratings_cleaned.csv')
    # iconicity_model = IconicityModel(csv_data)
    
    # # Mostrar las primeras 5 palabras del modelo
    # print("\nPrimeras 5 palabras del modelo de iconicidad:")
    # word_data = iconicity_model.get_all_word_data()
    # for i, (word, data) in enumerate(word_data.items()):
    #     if i >= 5:
    #         break
    #     print(f"\nPalabra: {word}")
    #     print(f"Datos: {data}")
    
    # # Mostrar estadísticas finales
    # print("\nProcesamiento completado.")
    # total_children_utterances = 0
    # total_adults_utterances = 0
    
    # for corpus_name in processed_data['Corpus_modified']:
    #     corpus_children = 0
    #     corpus_adults = 0
    #     for dir_name, content in processed_data['Corpus_modified'][corpus_name].items():
    #         if 'files' in content:
    #             for file in content['files']:
    #                 if 'children_data' in file:
    #                     corpus_children += len(file['children_data'])
    #                 if 'adults_data' in file:
    #                     corpus_adults += len(file['adults_data'])
        
    #     print(f"\nCorpus {corpus_name}:")
    #     print(f"  Total expresiones de niños: {corpus_children}")
    #     print(f"  Total expresiones de adultos: {corpus_adults}")
        
    #     total_children_utterances += corpus_children
    #     total_adults_utterances += corpus_adults
    
    # print(f"\nTotales globales:")
    # print(f"  Total expresiones de niños: {total_children_utterances}")
    # print(f"  Total expresiones de adultos: {total_adults_utterances}")

    # # Mostrar las expresiones tempranas de Lew
    # show_lew_early_expressions(processed_data)
    
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

def process_data_with_formatter(corpus_data):
    """
    Procesa los datos usando DataFormatter para separar datos de niños y adultos,
    manteniendo la estructura jerárquica del corpus.
    
    Args:
        corpus_data (dict): Datos del corpus a procesar
        
    Returns:
        dict: Estructura jerárquica con los datos separados por niños y adultos
    """
    # Crear instancias de DataFormatter para cada corpus
    brent_formatter = DataFormatter()
    newengland_formatter = DataFormatter()
    post_formatter = DataFormatter()
    vankleeck_formatter = DataFormatter()
    
    # Estructura resultante que mantendrá la jerarquía
    result = {'Corpus_modified': {}}
    
    # Procesar cada corpus
    for corpus_name in ['Brent', 'NewEngland', 'Post', 'VanKleeck']:
        if corpus_name in corpus_data['Corpus_modified']:
            result['Corpus_modified'][corpus_name] = {}
            corpus_data_current = corpus_data['Corpus_modified'][corpus_name]
            
            # Seleccionar el formatter correspondiente
            formatter = {
                'Brent': brent_formatter,
                'NewEngland': newengland_formatter,
                'Post': post_formatter,
                'VanKleeck': vankleeck_formatter
            }[corpus_name]
            
            # Procesar cada subdirectorio
            for dir_name, content in corpus_data_current.items():
                if 'files' in content:
                    result['Corpus_modified'][corpus_name][dir_name] = {
                        'files': []
                    }
                    
                    # Procesar cada archivo
                    for file in content['files']:
                        if file['metadata']['file_path'].endswith('.cha'):
                            file_path = file['metadata']['file_path']
                            children_data, adults_data = formatter.format_cha_data_from(file_path)
                            
                            # Crear una copia del archivo original con los datos separados
                            processed_file = {
                                'metadata': file['metadata'].copy(),
                                'children_data': children_data,
                                'adults_data': adults_data
                            }
                            
                            result['Corpus_modified'][corpus_name][dir_name]['files'].append(processed_file)
    
    return result

def show_lew_early_expressions(processed_data):
    """
    Muestra las expresiones de Lew cuando era más joven.
    
    Args:
        processed_data (dict): Datos procesados del corpus
    """
    print("\n=== Expresiones tempranas de Lew ===")
    
    # Buscar los archivos de Lew en el corpus Post
    if 'Post' in processed_data['Corpus_modified'] and 'Lew' in processed_data['Corpus_modified']['Post']:
        lew_files = processed_data['Corpus_modified']['Post']['Lew']['files']
        
        # Ordenar los archivos por edad
        sorted_files = sorted(lew_files, key=lambda x: x['metadata'].get('child_age', ''))
        
        # Mostrar las expresiones del archivo más antiguo
        if sorted_files:
            oldest_file = sorted_files[0]
            print(f"\nArchivo: {oldest_file['metadata']['file_path']}")
            print(f"Edad: {oldest_file['metadata'].get('child_age', 'N/A')}")
            print("\nPrimeras 20 expresiones de Lew:")
            
            # Mostrar las primeras 20 expresiones de Lew
            for i, (id, entry) in enumerate(list(oldest_file['children_data'].items())[:20]):
                print(f"\n{i+1}. {entry['text']}")
                if entry.get('timestamp'):
                    print(f"   Tiempo: {entry['timestamp']['start']}-{entry['timestamp']['end']}")

if __name__ == "__main__":
    main() 