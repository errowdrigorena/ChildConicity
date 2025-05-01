import os
import re
from datetime import datetime
from typing import Dict, List, Tuple

class BrentManipulator:
    def __init__(self, base_dir: str = "Brent", output_dir: str = "Brent_modified"):
        """
        Inicializa el manipulador de archivos Brent.
        
        Args:
            base_dir (str): Directorio base donde se encuentran los archivos Brent
            output_dir (str): Directorio donde se guardarán los archivos modificados
        """
        self.base_dir = base_dir
        self.output_dir = output_dir
        # Nombres confirmados
        self.child_names = {
            "c1": "Morgan",
            "s3": "Alan",
            "q1": "Quinn",
            "t1": "Alex",
            "w1": "Maggie",
            "w3": "Vasie",
            "v1": "Henry",
            "v2": "Xavier",
            "s2": "Tabitha",
            "m1": "Moomooshas",
            "j1": "Moomooshas",
            "i1": "Alexander",
            "d1": "Mandy",
            "f2": "Brooklyn",
            "f1": "Dillon",
            "s1": "Tymothy"
        }
        
    def process_directory(self) -> None:
        """
        Procesa el directorio base y crea la nueva estructura de directorios.
        """
        if not os.path.exists(self.base_dir):
            raise FileNotFoundError(f"El directorio {self.base_dir} no existe")
            
        # Crear directorio de salida si no existe
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        # Recorrer todos los subdirectorios
        for child_dir in os.listdir(self.base_dir):
            child_path = os.path.join(self.base_dir, child_dir)
            # Procesar solo directorios que empiecen con letra y tengan un número
            if os.path.isdir(child_path) and re.match(r'^[a-zA-Z]\d+$', child_dir):
                if child_dir not in self.child_names:
                    # Si no tenemos el nombre real, usar el código como nombre temporal
                    self.child_names[child_dir] = child_dir
                self._process_child_directory(child_dir)
                
    def _process_child_directory(self, child_dir: str) -> None:
        """
        Procesa un directorio específico de un niño.
        
        Args:
            child_dir (str): Nombre del directorio del niño (ej: c1, s3, etc.)
        """
        child_name = self.child_names[child_dir]
        output_child_dir = os.path.join(self.output_dir, child_name)
        
        # Crear directorio del niño si no existe
        if not os.path.exists(output_child_dir):
            os.makedirs(output_child_dir)
            
        # Procesar todos los archivos .cha en el directorio
        child_path = os.path.join(self.base_dir, child_dir)
        for filename in os.listdir(child_path):
            if filename.endswith('.cha'):
                self._process_cha_file(child_path, filename, output_child_dir)
                
    def _process_cha_file(self, input_dir: str, filename: str, output_dir: str) -> None:
        """
        Procesa un archivo .cha individual.
        
        Args:
            input_dir (str): Directorio de entrada
            filename (str): Nombre del archivo
            output_dir (str): Directorio de salida
        """
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        # Obtener el código del niño del directorio
        child_code = os.path.basename(input_dir)
        
        # Obtener el nombre del niño
        child_name = self.child_names.get(child_code, child_code)
        
        # Crear el directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)
        
        # Leer el archivo
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Calcular la edad
        age = self._calculate_age_from_filename(filename)
        
        # Insertar el metadato de edad
        content = self._insert_age_metadata(content, age, child_name)
        
        # Escribir el archivo modificado
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    def _calculate_age_from_filename(self, filename: str) -> Dict[str, int]:
        """
        Calcula la edad del niño basada en el nombre del archivo.
        Maneja dos formatos:
        1. AAMMDD.cha (ej: 010225.cha)
        2. x1-[r|f]DDmmmYY.cha (ej: m1-r15jun00.cha)
        
        Args:
            filename (str): Nombre del archivo
            
        Returns:
            Dict[str, int]: Diccionario con años, meses y días
        """
        # Quitar la extensión .cha
        base_name = filename.split('.')[0]
        
        try:
            # Intentar formato 1 (AAMMDD)
            if re.match(r'^\d{6}$', base_name):
                years = int(base_name[:2])
                months = int(base_name[2:4])
                days = int(base_name[4:6])
            # Intentar formato 2 (x1-[r|f]DDmmmYY)
            else:
                match = re.match(r'^[a-z]\d+-[rf](\d+)([a-z]+)(\d+)', base_name)
                if not match:
                    # Si no coincide con ningún formato, usar valores por defecto
                    return {"years": 0, "months": 0, "days": 0}
                    
                day = int(match.group(1))
                month_str = match.group(2).lower()
                year = int(match.group(3))
                
                # Convertir mes de texto a número
                month_map = {
                    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
                }
                
                if month_str not in month_map:
                    return {"years": 0, "months": 0, "days": 0}
                    
                months = month_map[month_str]
                years = year
                days = day
                
            return {
                "years": years,
                "months": months,
                "days": days
            }
        except (ValueError, IndexError):
            # Si hay algún error en la conversión, usar valores por defecto
            return {"years": 0, "months": 0, "days": 0}
        
    def _insert_age_metadata(self, content: str, age: Dict[str, int], child_name: str) -> str:
        """
        Inserta los metadatos de edad y nombre en el contenido del archivo.
        
        Args:
            content (str): Contenido del archivo
            age (Dict[str, int]): Diccionario con años, meses y días
            child_name (str): Nombre del niño
            
        Returns:
            str: Contenido con los metadatos añadidos
        """
        # Buscar la línea @Languages
        languages_index = content.find("@Languages")
        if languages_index == -1:
            return content
            
        # Insertar los metadatos después de @Languages
        metadata = f"@Child_Age: {age['years']:02d} years {age['months']:02d} months {age['days']:02d} days\n@ChildName: {child_name}\n"
        
        # Encontrar el final de la línea @Languages
        end_of_line = content.find('\n', languages_index)
        if end_of_line == -1:
            return content
            
        return content[:end_of_line + 1] + metadata + content[end_of_line + 1:] 