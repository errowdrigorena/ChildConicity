import os
import shutil
import re

def extract_age(file_path):
    """Extrae la edad del archivo .cha"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Buscar la línea que contiene la edad del niño
            match = re.search(r'@ID:\s*eng\|Post\|CHI\|(\d+;\d+\.\d+)\|', content)
            if match:
                age_str = match.group(1)
                # Convertir el formato 1;06.26 a años, meses y días
                years, rest = age_str.split(';')
                months, days = rest.split('.')
                return f"{years} years {months} months {days} days"
    except FileNotFoundError:
        return None
    return None

def modify_cha_file(file_path, child_name, age):
    """Modifica el archivo .cha para añadir los metadatos"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar la posición después de la línea @Languages
    languages_pos = content.find('@Languages:')
    if languages_pos == -1:
        return
    
    # Encontrar el final de la línea @Languages
    next_line_pos = content.find('\n', languages_pos)
    if next_line_pos == -1:
        return
    
    # Insertar los metadatos después de la línea @Languages
    new_content = (
        content[:next_line_pos + 1] +
        f'@ChildName: {child_name}\n' +
        f'@Child_Age: {age}\n' +
        content[next_line_pos + 1:]
    )
    
    # Escribir el contenido modificado
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def process_directory():
    """Procesa todos los archivos del directorio Post y crea Post_modified"""
    # Obtener el directorio raíz del proyecto
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    source_dir = os.path.join(root_dir, 'Post')
    target_dir = os.path.join(root_dir, 'Post_modified')
    
    # Crear el directorio objetivo si no existe
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Copiar los archivos de metadatos
    try:
        shutil.copy(os.path.join(source_dir, '0metadata.cdc'), os.path.join(target_dir, '0metadata.cdc'))
        shutil.copy(os.path.join(source_dir, '0types.txt'), os.path.join(target_dir, '0types.txt'))
    except FileNotFoundError:
        # En el caso de pruebas, estos archivos podrían no existir
        pass
    
    # Procesar cada subdirectorio
    for subdir in os.listdir(source_dir):
        source_subdir = os.path.join(source_dir, subdir)
        if not os.path.isdir(source_subdir) or subdir.startswith('.'):
            continue
        
        # Crear el subdirectorio en el directorio objetivo
        target_subdir = os.path.join(target_dir, subdir)
        if not os.path.exists(target_subdir):
            os.makedirs(target_subdir)
        
        # Procesar cada archivo .cha en el subdirectorio
        for file in os.listdir(source_subdir):
            if not file.endswith('.cha'):
                continue
            
            source_file = os.path.join(source_subdir, file)
            target_file = os.path.join(target_subdir, file)
            
            # Copiar el archivo
            shutil.copy2(source_file, target_file)
            
            # Extraer la edad y modificar el archivo
            age = extract_age(source_file)
            if age:
                modify_cha_file(target_file, subdir, age)
                print(f"Procesado {source_file} -> {target_file}")

if __name__ == '__main__':
    process_directory() 