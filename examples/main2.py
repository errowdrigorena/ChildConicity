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
from src.data_analysis_plotter import DataAnalysisPlotter

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
        
        # Asegurar que los meses estén en el rango 0-11
        months = months % 12
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
                        
                        # Generar claves únicas para los datos de niños y adultos
                        child_base = len(data_grouped_by_age[age_quarter]['children_data'])
                        adult_base = len(data_grouped_by_age[age_quarter]['adults_data'])
                        
                        # Añadir los datos de niños con claves únicas
                        for i, (_, utterance) in enumerate(file['children_data'].items()):
                            key = f"{child_base + i + 1}"
                            data_grouped_by_age[age_quarter]['children_data'][key] = utterance
                        
                        # Añadir los datos de adultos con claves únicas
                        for i, (_, utterance) in enumerate(file['adults_data'].items()):
                            key = f"{adult_base + i + 1}"
                            data_grouped_by_age[age_quarter]['adults_data'][key] = utterance
                        
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

def create_age_group_statistics(data_grouped_by_age, iconicity_model):
    """
    Crea un diccionario con estadísticas de palabras e iconicidad por grupo de edad.
    
    Args:
        data_grouped_by_age (dict): Datos agrupados por edad
        iconicity_model (IconicityModel): Modelo de iconicidad
        
    Returns:
        dict: Estadísticas por grupo de edad
    """
    age_group_stats = {}
    
    # Obtener todas las palabras con iconicidad del modelo
    all_iconicity_words = iconicity_model.get_all_word_data()
    
    for age_group, data in data_grouped_by_age.items():
        # Crear contadores de palabras para niños y adultos
        children_counter = WordCounter()
        adults_counter = WordCounter()
        
        # Contar palabras de niños
        for utterance in data['children_data'].values():
            children_counter.count_words(utterance['text'])
        
        # Contar palabras de adultos
        for utterance in data['adults_data'].values():
            adults_counter.count_words(utterance['text'])
        
        # Crear entrada en el diccionario
        age_group_stats[age_group] = {
            'age_group': age_group,
            'children_counted_words': children_counter.get_word_counts(),
            'adults_counted_words': adults_counter.get_word_counts(),
            'all_iconicity_words': all_iconicity_words
        }
    
    return age_group_stats

def print_age_group_statistics(age_group_stats, num_words=10):
    """
    Imprime las estadísticas de palabras por grupo de edad.
    
    Args:
        age_group_stats (dict): Estadísticas por grupo de edad
        num_words (int): Número de palabras más frecuentes a mostrar
    """
    for age_group, stats in sorted(age_group_stats.items()):
        print(f"\n=== Grupo de edad {age_group} ===")
        
        # Palabras más frecuentes de niños
        print("\nTop palabras de niños:")
        children_words = sorted(stats['children_counted_words'].items(), 
                             key=lambda x: x[1], reverse=True)[:num_words]
        for word, count in children_words:
            print(f"  {word}: {count}")
        
        # Palabras más frecuentes de adultos
        print("\nTop palabras de adultos:")
        adults_words = sorted(stats['adults_counted_words'].items(), 
                            key=lambda x: x[1], reverse=True)[:num_words]
        for word, count in adults_words:
            print(f"  {word}: {count}")
        
        # Estadísticas de palabras con iconicidad
        children_iconic = set(word for word in stats['children_counted_words'].keys() if word in stats['all_iconicity_words'])
        adults_iconic = set(word for word in stats['adults_counted_words'].keys() if word in stats['all_iconicity_words'])
        
        print(f"\nEstadísticas de iconicidad:")
        print(f"  Palabras con iconicidad usadas por niños: {len(children_iconic)}")
        print(f"  Palabras con iconicidad usadas por adultos: {len(adults_iconic)}")
        print("-" * 50)

def process_valid_words_by_age_group(age_group_stats, iconicity_model):
    """
    Procesa las palabras válidas por grupo de edad, clasificándolas en icónicas y no icónicas.
    
    Args:
        age_group_stats (dict): Estadísticas por grupo de edad
        iconicity_model (IconicityModel): Modelo de iconicidad
        
    Returns:
        dict: Estadísticas de palabras válidas por grupo de edad
    """
    valid_words_stats = {}
    all_iconicity_words = iconicity_model.get_all_word_data()
    
    for age_group, stats in age_group_stats.items():
        # Inicializar contadores para este grupo de edad
        group_stats = {
            'adults': {
                'total_words': 0,
                'iconic_words': {},
                'non_iconic_words': {},
                'total_iconic_occurrences': 0,
                'total_non_iconic_occurrences': 0,
                'unique_iconic_words': set(),
                'unique_non_iconic_words': set()
            },
            'children': {
                'total_words': 0,
                'iconic_words': {},
                'non_iconic_words': {},
                'total_iconic_occurrences': 0,
                'total_non_iconic_occurrences': 0,
                'unique_iconic_words': set(),
                'unique_non_iconic_words': set()
            }
        }
        
        # Procesar palabras de adultos
        for word, count_data in stats['adults_counted_words'].items():
            count = count_data['count']
            group_stats['adults']['total_words'] += count
            if word in all_iconicity_words:
                group_stats['adults']['iconic_words'][word] = {
                    'count': count,
                    'rating': all_iconicity_words[word]['rating']
                }
                group_stats['adults']['total_iconic_occurrences'] += count
                group_stats['adults']['unique_iconic_words'].add(word)
            else:
                group_stats['adults']['non_iconic_words'][word] = count
                group_stats['adults']['total_non_iconic_occurrences'] += count
                group_stats['adults']['unique_non_iconic_words'].add(word)
        
        # Procesar palabras de niños
        for word, count_data in stats['children_counted_words'].items():
            count = count_data['count']
            group_stats['children']['total_words'] += count
            if word in all_iconicity_words:
                group_stats['children']['iconic_words'][word] = {
                    'count': count,
                    'rating': all_iconicity_words[word]['rating']
                }
                group_stats['children']['total_iconic_occurrences'] += count
                group_stats['children']['unique_iconic_words'].add(word)
            else:
                group_stats['children']['non_iconic_words'][word] = count
                group_stats['children']['total_non_iconic_occurrences'] += count
                group_stats['children']['unique_non_iconic_words'].add(word)
        
        valid_words_stats[age_group] = group_stats
    
    return valid_words_stats

def print_valid_words_statistics(valid_words_stats):
    """
    Imprime las estadísticas de palabras válidas por grupo de edad.
    
    Args:
        valid_words_stats (dict): Estadísticas de palabras válidas por grupo de edad
    """
    for age_group, stats in sorted(valid_words_stats.items()):
        print(f"\n=== Grupo de edad {age_group} ===")
        
        # Estadísticas de adultos
        print("\nEstadísticas de adultos:")
        print(f"  Total de palabras: {stats['adults']['total_words']}")
        
        # Calcular totales de ocurrencias de palabras icónicas y no icónicas
        total_iconic_occurrences_adults = stats['adults']['total_iconic_occurrences']
        total_non_iconic_occurrences_adults = stats['adults']['total_non_iconic_occurrences']
        
        print(f"  Número total de ocurrencias de palabras icónicas: {total_iconic_occurrences_adults}")
        print(f"  Número total de ocurrencias de palabras no icónicas: {total_non_iconic_occurrences_adults}")
        print(f"  Número de palabras icónicas diferentes: {len(stats['adults']['iconic_words'])}")
        print(f"  Número de palabras no icónicas diferentes: {len(stats['adults']['non_iconic_words'])}")
        
        # Estadísticas de niños
        print("\nEstadísticas de niños:")
        print(f"  Total de palabras: {stats['children']['total_words']}")
        
        # Calcular totales de ocurrencias de palabras icónicas y no icónicas
        total_iconic_occurrences_children = stats['children']['total_iconic_occurrences']
        total_non_iconic_occurrences_children = stats['children']['total_non_iconic_occurrences']
        
        print(f"  Número total de ocurrencias de palabras icónicas: {total_iconic_occurrences_children}")
        print(f"  Número total de ocurrencias de palabras no icónicas: {total_non_iconic_occurrences_children}")
        print(f"  Número de palabras icónicas diferentes: {len(stats['children']['iconic_words'])}")
        print(f"  Número de palabras no icónicas diferentes: {len(stats['children']['non_iconic_words'])}")
        
        # Top 10 palabras icónicas más usadas por adultos
        print("\nTop 10 palabras icónicas más usadas por adultos:")
        adult_iconic = sorted(stats['adults']['iconic_words'].items(), 
                            key=lambda x: x[1]['count'], reverse=True)[:10]
        for word, data in adult_iconic:
            print(f"  {word}: {data['count']} usos, rating: {data['rating']}")
        
        # Top 10 palabras icónicas más usadas por niños
        print("\nTop 10 palabras icónicas más usadas por niños:")
        child_iconic = sorted(stats['children']['iconic_words'].items(), 
                            key=lambda x: x[1]['count'], reverse=True)[:10]
        for word, data in child_iconic:
            print(f"  {word}: {data['count']} usos, rating: {data['rating']}")
        print("-" * 50)

        # Top 10 palabras no icónicas más usadas por niños
        print("\nTop 10 palabras NO icónicas más usadas por niños:")
        child_non_iconic = sorted(stats['children']['non_iconic_words'].items(), 
                            key=lambda x: x[1], reverse=True)[:10]
        for word, count in child_non_iconic:
            print(f"  {word}: {count} usos")
        print("-" * 50)

                # Top 10 palabras no icónicas más usadas por niños
        print("\nTop 10 palabras NO icónicas más usadas por adultos:")
        child_non_iconic = sorted(stats['adults']['non_iconic_words'].items(), 
                            key=lambda x: x[1], reverse=True)[:10]
        for word, count in child_non_iconic:
            print(f"  {word}: {count} usos")
        print("-" * 50)

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
    
    # Crear el modelo de iconicidad
    print("\nCreando modelo de iconicidad...")
    formatter = DataFormatter()
    csv_data = formatter.format_csv_data_from('iconicity_ratings_cleaned.csv')
    iconicity_model = IconicityModel(csv_data)
    
    # Crear estadísticas por grupo de edad
    print("\nCreando estadísticas por grupo de edad...")
    age_group_stats_raw = create_age_group_statistics(data_grouped_by_age, iconicity_model)
    
    # Procesar palabras válidas por grupo de edad
    print("\nProcesando palabras válidas por grupo de edad...")
    valid_words_stats = process_valid_words_by_age_group(age_group_stats_raw, iconicity_model)
    
    # Mostrar estadísticas de palabras válidas
    print("\nMostrando estadísticas de palabras válidas por grupo de edad:")
    print_valid_words_statistics(valid_words_stats)
    
    # Crear y mostrar gráficas de análisis
    print("\nCreando gráficas de análisis...")
    plotter = DataAnalysisPlotter(valid_words_stats)
    
    # Gráfica general sin porcentajes
    plotter.plot_iconic_vs_non_iconic_by_age('iconic_vs_non_iconic_by_age.png')
    
    # Gráficas separadas con porcentajes
    plotter.plot_iconic_vs_non_iconic_by_age_adults('iconic_vs_non_iconic_by_age_adults.png')
    plotter.plot_iconic_vs_non_iconic_by_age_children('iconic_vs_non_iconic_by_age_children.png')
    
    # Mostrar porcentajes de palabras icónicas y no icónicas para adultos
    print("\nPorcentajes de palabras icónicas y no icónicas para adultos por grupo de edad:")
    for age_group, stats in sorted(valid_words_stats.items()):
        total_adults = stats['adults']['total_words']
        iconic_pct = (stats['adults']['total_iconic_occurrences'] / total_adults * 100) if total_adults > 0 else 0
        non_iconic_pct = (stats['adults']['total_non_iconic_occurrences'] / total_adults * 100) if total_adults > 0 else 0
        print(f"\nGrupo de edad {age_group}:")
        print(f"  Palabras icónicas: {iconic_pct:.1f}%")
        print(f"  Palabras no icónicas: {non_iconic_pct:.1f}%")

if __name__ == "__main__":
    main() 