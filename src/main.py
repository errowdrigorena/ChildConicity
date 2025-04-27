from src.reader import Reader
from src.data_formatter import DataFormatter
from src.word_counter import WordCounter
from src.iconicity_model import IconicityModel
from src.word_dictionary_merger import WordDictionaryMerger

if __name__ == "__main__":
    # Procesar archivo CSV
    print("Procesando archivo CSV:")
    formatter = DataFormatter()
    csv_data = formatter.format_csv_data_from('iconicity_ratings_cleaned.csv')
    if csv_data is not None:
        print("\nPrimeras 5 entradas del CSV:")
        for id, entry in list(csv_data.items())[:5]:
            print(f"\n{id}:")
            for key, value in entry.items():
                print(f"{key}: {value}")
    
    print("\n" + "="*50 + "\n")
    
    # Procesar archivo .cha
    print("Procesando archivo .cha:")
    children_data, adults_data = formatter.format_cha_data_from('record.cha')
    
    print("\nPrimeras 10 expresiones de niños:")
    for id, entry in list(children_data.items())[:10]:
        print(f"\n{id}:")
        print(f"  Hablante: {entry['speaker']}")
        print(f"  Texto: {entry['text']}")
        if entry['timestamp']:
            print(f"  Tiempo: {entry['timestamp']['start']}-{entry['timestamp']['end']}")
    
    print("\n" + "="*50 + "\n")
    
    print("Primeras 10 expresiones de adultos:")
    for id, entry in list(adults_data.items())[:10]:
        print(f"\n{id}:")
        print(f"  Hablante: {entry['speaker']}")
        print(f"  Texto: {entry['text']}")
        if entry['timestamp']:
            print(f"  Tiempo: {entry['timestamp']['start']}-{entry['timestamp']['end']}")
    
    print("\n" + "="*50 + "\n")
    
    # Mostrar metadatos del archivo .cha
    print("Metadatos del archivo .cha:")
    reader = Reader()
    cha_data = reader.read_cha('record.cha')
    if cha_data is not None:
        metadata = cha_data['metadata']
        print(f"Codificación: {metadata['encoding']}")
        print(f"PID: {metadata['pid']}")
        print(f"Idiomas: {', '.join(metadata['languages'])}")
        print("\nParticipantes:")
        for code, name in metadata['participants'].items():
            print(f"  {code}: {name}")
        print(f"\nOpciones: {', '.join(metadata['options'])}")
        print(f"Medios: {metadata['media']['id']} ({metadata['media']['type']})")
        print(f"Fecha: {metadata['date']}")
        print(f"Tipos: {', '.join(metadata['types'])}")
    
    print("\n" + "="*50 + "\n")
    
    # Análisis de palabras
    print("Análisis de palabras:")
    
    # Contar palabras en las expresiones de niños
    print("\nPalabras más comunes en niños:")
    child_counter = WordCounter()
    child_counts = child_counter.count_words(children_data)
    print("\n10 palabras más comunes en niños:")
    for word, count in child_counter.get_most_common(10):
        print(f"{word}: {count} veces")
    
    print("\n" + "="*50 + "\n")
    
    # Contar palabras en las expresiones de adultos
    print("Palabras más comunes en adultos:")
    adult_counter = WordCounter()
    adult_counts = adult_counter.count_words(adults_data)
    print("\n10 palabras más comunes en adultos:")
    for word, count in adult_counter.get_most_common(10):
        print(f"{word}: {count} veces")
    
    print("\n" + "="*50 + "\n")
    
    # Análisis de iconicidad
    print("Análisis de iconicidad:")
    
    # Verificar el contenido de csv_data
    print("\nVerificación de datos CSV:")
    if csv_data is None:
        print("Error: No se pudieron cargar los datos del CSV")
    else:
        print(f"Total de entradas en CSV: {len(csv_data)}")
        if len(csv_data) > 0:
            first_entry = next(iter(csv_data.values()))
            print("\nEstructura de una entrada:")
            for key, value in first_entry.items():
                print(f"{key}: {value}")
    
    # Crear el modelo de iconicidad
    iconicity_model = IconicityModel(csv_data)
    
    # Verificar el contenido del modelo
    print("\nVerificación del modelo de iconicidad:")
    all_words = iconicity_model.get_all_word_data()
    
    # Crear instancia de WordDictionaryMerger y añadir diccionarios
    merger = WordDictionaryMerger()
    merger.add_dictionary(all_words)
    merger.add_dictionary(adult_counts)
    # merger.add_dictionary(child_counts)
    
    # Obtener el merge
    merged_dict, unmerged_dictionaries = merger.obtain_merge()
    
    # Mostrar algunas estadísticas
    print("\nEstadísticas del merge:")
    print(f"Número de palabras en el diccionario mergeado: {len(merged_dict)}")
    print(f"Número de diccionarios no mergeados: {len(unmerged_dictionaries)}")
    
    # Mostrar algunas palabras del diccionario mergeado
    print("\nEjemplos de palabras en el diccionario mergeado:")
    for i, (word, data) in enumerate(merged_dict.items()):
        if i < 5:  # Mostrar solo las primeras 5 palabras
            print(f"\nPalabra: {word}")
            print(f"Datos: {data}")

    # Ordenar el diccionario mergeado por rating de mayor a menor
    print("\nDiccionario mergeado ordenado por rating (de mayor a menor):")
    sorted_merged_dict = dict(sorted(
        merged_dict.items(),
        key=lambda x: x[1]['rating'],
        reverse=True
    ))
    
    # Mostrar las primeras 10 palabras ordenadas
    print("\nTop 10 palabras por rating:")
    for i, (word, data) in enumerate(sorted_merged_dict.items()):
        if i >= 10:
            break
        print(f"{word}: Rating={data['rating']}, Count={data.get('count', 0)}")    

    # Leer el DirectorioBrent
    print("\n" + "="*50 + "\n")
    print("Leyendo Brent:")
    reader = Reader()
    brent_data = reader.read_directory('Brent')
    
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
    
    # Mostrar la estructura del directorio
    print("\nEstructura de Brent:")
    print_directory_structure(brent_data)

    # Mostrar el contenido de un archivo específico
    print("\n" + "="*50 + "\n")
    print("Contenido del primer archivo encontrado:")
    
    # Obtener el contenido del primer archivo que encontremos
    first_file = None
    for dir_name, content in brent_data['Brent'].items():
        if 'files' in content and content['files']:
            first_file = content['files'][0]
            print(f"Archivo: {first_file['metadata']['file_path']}")
            break
    
    if first_file:
        # Mostrar metadatos
        print("\nMetadatos:")
        for key, value in first_file['metadata'].items():
            print(f"{key}: {value}")
        
        # Procesar el archivo usando DataFormatter
        print("\nProcesando archivo con DataFormatter:")
        file_path = first_file['metadata']['file_path']
        children_data, adults_data = formatter.format_cha_data_from(file_path)
        
        print("\nPrimeras 10 expresiones de niños:")
        for id, entry in list(children_data.items())[:10]:
            print(f"\n{id}:")
            print(f"  Hablante: {entry['speaker']}")
            print(f"  Texto: {entry['text']}")
            if entry['timestamp']:
                print(f"  Tiempo: {entry['timestamp']['start']}-{entry['timestamp']['end']}")
        
        print("\nPrimeras 10 expresiones de adultos:")
        for id, entry in list(adults_data.items())[:10]:
            print(f"\n{id}:")
            print(f"  Hablante: {entry['speaker']}")
            print(f"  Texto: {entry['text']}")
            if entry['timestamp']:
                print(f"  Tiempo: {entry['timestamp']['start']}-{entry['timestamp']['end']}")

