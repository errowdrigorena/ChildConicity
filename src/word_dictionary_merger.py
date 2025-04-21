class WordDictionaryMerger:
    def __init__(self):
        """
        Inicializa el merger con un array vacío de diccionarios.
        """
        self.dictionaries = []
    
    def add_dictionary(self, dictionary):
        """
        Añade un nuevo diccionario al array.
        
        Args:
            dictionary (dict): Diccionario que tiene strings como claves principales
        """
        if not isinstance(dictionary, dict):
            raise ValueError("El parámetro debe ser un diccionario")
        self.dictionaries.append(dictionary)
    
    def obtain_merge(self):
        """
        Obtiene dos resultados:
        1. Un diccionario con las palabras que aparecen en todos los diccionarios, mergeando sus datos
        2. Un array con los diccionarios de palabras que no se pudieron mergear
        
        Returns:
            tuple: (merged_dict, unmerged_dictionaries)
        """
        if not self.dictionaries:
            return {}, []
        
        # Obtener todas las palabras únicas
        all_words = set()
        for dictionary in self.dictionaries:
            all_words.update(dictionary.keys())
        
        # Encontrar palabras comunes a todos los diccionarios
        common_words = set(all_words)
        for dictionary in self.dictionaries:
            common_words.intersection_update(dictionary.keys())
        
        # Crear el diccionario mergeado
        merged_dict = {}
        for word in common_words:
            merged_data = {}
            for dictionary in self.dictionaries:
                merged_data.update(dictionary[word])
            merged_dict[word] = merged_data
        
        # Crear los diccionarios no mergeados
        unmerged_dictionaries = []
        for dictionary in self.dictionaries:
            unmerged_dict = {}
            for word, data in dictionary.items():
                if word not in common_words:
                    unmerged_dict[word] = data
            if unmerged_dict:  # Solo añadir si hay palabras no mergeadas
                unmerged_dictionaries.append(unmerged_dict)
        
        return merged_dict, unmerged_dictionaries 