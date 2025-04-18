import pandas as pd
import re

class Reader:
    def __init__(self):
        self.data = None
    
    def read_csv(self, file_path):
        """
        Lee un archivo CSV y lo almacena en el atributo data.
        
        Args:
            file_path (str): Ruta del archivo CSV a leer
            
        Returns:
            pandas.DataFrame: Los datos leídos del archivo CSV
        """
        try:
            self.data = pd.read_csv(file_path)
            return self.data
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {file_path}")
            return None
        except Exception as e:
            print(f"Error al leer el archivo CSV: {str(e)}")
            return None

    def read_cha(self, file_path):
        """
        Lee un archivo .cha y lo convierte a un formato estructurado.
        
        Args:
            file_path (str): Ruta del archivo .cha a leer
            
        Returns:
            dict: Diccionario con los datos estructurados del archivo .cha
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Extraer metadatos del archivo
            metadata = {
                'file_path': file_path,
                'file_type': 'cha',
                'encoding': self._extract_encoding(content),
                'pid': self._extract_pid(content),
                'languages': self._extract_languages(content),
                'participants': self._extract_participants(content),
                'options': self._extract_options(content),
                'media': self._extract_media(content),
                'date': self._extract_date(content),
                'types': self._extract_types(content),
                'utterances': self._extract_utterances(content)
            }
            
            self.data = {
                'content': content,
                'metadata': metadata
            }
            return self.data
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {file_path}")
            return None
        except Exception as e:
            print(f"Error al leer el archivo .cha: {str(e)}")
            return None

    def _extract_encoding(self, content):
        """Extrae la codificación del archivo."""
        match = re.search(r'@UTF8', content)
        return 'UTF8' if match else None

    def _extract_pid(self, content):
        """Extrae el PID del archivo."""
        match = re.search(r'@PID:\s*(.*)', content)
        return match.group(1).strip() if match else None

    def _extract_languages(self, content):
        """Extrae los idiomas del archivo."""
        match = re.search(r'@Languages:\s*(.*)', content)
        return match.group(1).strip().split(',') if match else []

    def _extract_participants(self, content):
        """Extrae los participantes del archivo."""
        match = re.search(r'@Participants:\s*(.*)', content)
        if match:
            participants = {}
            for part in match.group(1).strip().split(','):
                code, name = part.strip().split(' ', 1)
                participants[code] = name
            return participants
        return {}

    def _extract_options(self, content):
        """Extrae las opciones del archivo."""
        match = re.search(r'@Options:\s*(.*)', content)
        return match.group(1).strip().split(',') if match else []

    def _extract_media(self, content):
        """Extrae la información de medios del archivo."""
        match = re.search(r'@Media:\s*(.*)', content)
        if match:
            media_info = match.group(1).strip().split(',')
            return {
                'id': media_info[0].strip(),
                'type': media_info[1].strip() if len(media_info) > 1 else None
            }
        return None

    def _extract_date(self, content):
        """Extrae la fecha del archivo."""
        match = re.search(r'@Date:\s*(.*)', content)
        return match.group(1).strip() if match else None

    def _extract_types(self, content):
        """Extrae los tipos del archivo."""
        match = re.search(r'@Types:\s*(.*)', content)
        return match.group(1).strip().split(',') if match else []

    def _extract_utterances(self, content):
        """Extrae las expresiones del archivo."""
        utterances = []
        for line in content.split('\n'):
            if line.startswith('*'):
                speaker, text = line.split(':', 1)
                speaker = speaker[1:].strip()  # Eliminar el asterisco
                # Extraer la marca de tiempo y limpiar el texto
                timestamp = self._extract_timestamp(text)
                # Eliminar la marca de tiempo del texto
                clean_text = re.sub(r'\d+_\d+', '', text).strip()
                utterances.append({
                    'speaker': speaker,
                    'text': clean_text,
                    'timestamp': timestamp
                })
        return utterances

    def _extract_timestamp(self, text):
        """Extrae la marca de tiempo de una expresión."""
        match = re.search(r'(\d+)_(\d+)', text)
        if match:
            return {
                'start': int(match.group(1)),
                'end': int(match.group(2))
            }
        return None 