import re
from collections import defaultdict

class WordCounter:
    def __init__(self):
        self.word_counts = defaultdict(int)
    
    def count_words(self, data_dict):
        """
        Cuenta las ocurrencias de cada palabra en los campos 'text' de un diccionario.
        
        Args:
            data_dict (dict): Diccionario con entradas que contienen un campo 'text'
            
        Returns:
            dict: Diccionario con palabras como claves y su número de ocurrencias como valores
        """
        self.word_counts.clear()  # Limpiar contadores anteriores
        
        for entry in data_dict.values():
            if 'text' in entry and isinstance(entry['text'], str):
                # Dividir el texto en palabras, eliminando puntuación y convirtiendo a minúsculas
                words = re.findall(r'\b\w+\b', entry['text'].lower())
                for word in words:
                    self.word_counts[word] += 1
        
        return dict(self.word_counts)
    
    def get_word_counts(self):
        """
        Devuelve el diccionario con los conteos de palabras.
        
        Returns:
            dict: Diccionario con palabras como claves y su número de ocurrencias como valores
        """
        return dict(self.word_counts)
    
    def get_most_common(self, n=10):
        """
        Devuelve las n palabras más comunes.
        
        Args:
            n (int): Número de palabras más comunes a devolver
            
        Returns:
            list: Lista de tuplas (palabra, conteo) ordenadas por frecuencia descendente
        """
        return sorted(self.word_counts.items(), key=lambda x: x[1], reverse=True)[:n] 