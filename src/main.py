from src.reader import Reader
from src.data_formatter import DataFormatter
from src.word_counter import WordCounter
from src.iconicity_model import IconicityModel

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
    iconicity_model = IconicityModel(csv_data)
    print("\nDatos de las primeras 5 palabras:")
    for word in list(iconicity_model.get_all_words())[:5]:
        data = iconicity_model.get_word_data(word)
        print(f"\nPalabra: {word}")
        print(f"  n_ratings: {data['n_ratings']}")
        print(f"  n: {data['n']}")
        print(f"  prop_knwn: {data['prop_knwn']:.2f}")
        print(f"  rating: {data['rating']:.2f}")
        print(f"  rating_sd: {data['rating_sd']:.2f}") 