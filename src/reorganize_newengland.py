import os
import shutil

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
            
            print(f'Copiado {source_file} a {target_file}')

print('Reorganización completada') 