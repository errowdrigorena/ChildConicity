import os
import re
from src.data_formatter import DataFormatter

class CorpusManipulator:
    """Manipulador genérico para todos los corpus"""
    
    def __init__(self):
        self.base_dir = None
        self.formatter = DataFormatter()
    
    def process_directory(self):
        """Procesa el directorio del corpus"""
        if not self.base_dir:
            raise ValueError("base_dir no está configurado")
            
        # Procesar todos los archivos .cha en el directorio
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith('.cha'):
                    file_path = os.path.join(root, file)
                    self.process_file(file_path)
    
    def process_file(self, file_path):
        """Procesa un archivo .cha individual"""
        # Extraer la edad del archivo
        age = self.extract_age(file_path)
        
        # Modificar el archivo con la edad extraída
        self.modify_file(file_path, age)
    
    def extract_age(self, file_path):
        """Extrae la edad del archivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Buscar la línea que contiene la edad
            age_pattern = r'\*CHI:\s*.*?(\d+)[;:]'
            match = re.search(age_pattern, content)
            
            if match:
                return match.group(1)
            return None
        except Exception as e:
            print(f"Error al extraer la edad de {file_path}: {str(e)}")
            return None
    
    def modify_file(self, file_path, age):
        """Modifica el archivo con la edad extraída"""
        if age is None:
            return
            
        try:
            # Leer el contenido del archivo
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Modificar el contenido con la edad
            modified_content = self.add_age_to_content(content, age)
            
            # Guardar el archivo modificado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
                
            print(f"Archivo modificado exitosamente: {file_path}")
        except Exception as e:
            print(f"Error al modificar el archivo {file_path}: {str(e)}")
    
    def add_age_to_content(self, content, age):
        """Añade la edad al contenido del archivo"""
        # Buscar la línea que contiene la edad
        age_pattern = r'(\*CHI:\s*.*?)(\d+)([;:])'
        
        # Reemplazar la edad con el nuevo valor
        modified_content = re.sub(age_pattern, f'\\1{age}\\3', content)
        
        return modified_content 