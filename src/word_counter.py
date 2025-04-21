import re
from collections import defaultdict

class WordCounter:
    """
    Clase para contar palabras en un diccionario de datos.
    """
    
    def __init__(self):
        """
        Inicializa el contador de palabras.
        """
        self.word_counts = defaultdict(int)
    
    def count_words(self, data_dict):
        """
        Cuenta las palabras en los campos 'text' del diccionario.
        
        Args:
            data_dict (dict): Diccionario con campos 'text' para procesar.
            
        Returns:
            dict: Diccionario con palabras como claves y diccionarios de conteo como valores.
                 Formato: {'palabra': {'count': N}}
        """
        # Reiniciar el contador
        self.word_counts.clear()
        
        # Contar palabras en cada entrada
        for entry in data_dict.values():
            if 'text' in entry:
                # Encontrar todas las palabras usando regex
                words = re.findall(r'\b\w+\b', entry['text'].lower())
                for word in words:
                    self.word_counts[word] += 1
        
        # Convertir el defaultdict a un diccionario con el formato deseado
        return {word: {'count': count} for word, count in self.word_counts.items()}
    
    def get_word_counts(self):
        """
        Obtiene el diccionario de conteo de palabras.
        
        Returns:
            dict: Diccionario con palabras como claves y sus conteos como valores.
        """
        return dict(self.word_counts)
    
    def get_most_common(self, n=10):
        """
        Obtiene las n palabras más comunes.
        
        Args:
            n (int): Número de palabras a retornar.
            
        Returns:
            list: Lista de tuplas (palabra, conteo) ordenadas por frecuencia.
        """
        # Ordenar por conteo y luego alfabéticamente para desempates
        return sorted(self.word_counts.items(), 
                     key=lambda x: (-x[1], x[0]))[:n] 