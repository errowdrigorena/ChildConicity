import os
import shutil
import re

def extract_age(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Buscar la línea que contiene la edad del niño
        match = re.search(r'@ID:\s*eng\|NewEngland\|CHI\|(\d+;\d+\.\d+)\|', content)
        if match:
            age_str = match.group(1)
            # Convertir el formato 1;06.26 a años, meses y días
            years, rest = age_str.split(';')
            months, days = rest.split('.')
            return f"{years} years {months} months {days} days"
    return None

def modify_cha_file(file_path, child_name, age):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar la posición después de @Languages
    languages_pos = content.find('@Languages:')
    if languages_pos != -1:
        # Encontrar el final de la línea @Languages
        end_of_line = content.find('\n', languages_pos)
        if end_of_line != -1:
            # Insertar los metadatos después de @Languages
            new_content = content[:end_of_line + 1] + f'@ChildName: {child_name}\n@Child_Age: {age}\n' + content[end_of_line + 1:]
            
            # Escribir el contenido modificado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

# Directorios de origen y destino
source_dir = '../NewEngland'
target_dir = '../NewEngland_modified'

# Crear el directorio de destino si no existe
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Obtener todas las subcarpetas de NewEngland
subdirs = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]

# Para cada subcarpeta
for subdir in subdirs:
    subdir_path = os.path.join(source_dir, subdir)
    
    # Para cada archivo .cha en la subcarpeta
    for file in os.listdir(subdir_path):
        if file.endswith('.cha'):
            # Extraer el número del archivo (sin la extensión)
            file_number = file.split('.')[0]
            
            # Crear el nombre de la carpeta de destino
            target_folder = f'Target{file_number}'
            target_folder_path = os.path.join(target_dir, target_folder)
            
            # Crear la carpeta de destino si no existe
            if not os.path.exists(target_folder_path):
                os.makedirs(target_folder_path)
            
            # Crear el nuevo nombre del archivo
            new_filename = f'{subdir}.cha'
            
            # Copiar y renombrar el archivo
            source_file = os.path.join(subdir_path, file)
            target_file = os.path.join(target_folder_path, new_filename)
            shutil.copy2(source_file, target_file)
            
            # Extraer la edad y modificar el archivo .cha
            age = extract_age(source_file)
            if age:
                modify_cha_file(target_file, target_folder, age)
            
            print(f'Copiado y modificado {source_file} a {target_file}')

print('Reorganización completada') 