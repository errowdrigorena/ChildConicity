import os
import pytest
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

def test_extract_age():
    # Caso 1: Edad válida
    test_content = "@ID: eng|NewEngland|CHI|1;06.26|male|TD||Target_Child|||"
    test_file = "test_age.cha"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    expected_age = "1 years 06 months 26 days"
    assert extract_age(test_file) == expected_age
    
    # Caso 2: Archivo sin edad
    test_content = "@ID: eng|NewEngland|CHI||male|TD||Target_Child|||"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    assert extract_age(test_file) is None
    
    # Caso 3: Archivo vacío
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("")
    
    assert extract_age(test_file) is None
    
    # Limpieza
    os.remove(test_file)

def test_modify_cha_file():
    # Preparar archivo de prueba
    test_content = """@UTF8
@PID: test
@Begin
@Languages: eng
@Participants: INV Investigator, CHI Target_Child
@ID: eng|NewEngland|CHI|1;06.26|male|TD||Target_Child|||
"""
    test_file = "test_modify.cha"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    # Probar la modificación
    child_name = "Target01"
    age = "1 years 06 months 26 days"
    modify_cha_file(test_file, child_name, age)
    
    # Verificar el resultado
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    expected_content = """@UTF8
@PID: test
@Begin
@Languages: eng
@ChildName: Target01
@Child_Age: 1 years 06 months 26 days
@Participants: INV Investigator, CHI Target_Child
@ID: eng|NewEngland|CHI|1;06.26|male|TD||Target_Child|||
"""
    assert content == expected_content
    
    # Limpieza
    os.remove(test_file)

def test_modify_cha_file_without_languages():
    # Preparar archivo de prueba sin línea @Languages
    test_content = """@UTF8
@PID: test
@Begin
@Participants: INV Investigator, CHI Target_Child
@ID: eng|NewEngland|CHI|1;06.26|male|TD||Target_Child|||
"""
    test_file = "test_modify_no_lang.cha"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    # Probar la modificación
    child_name = "Target01"
    age = "1 years 06 months 26 days"
    modify_cha_file(test_file, child_name, age)
    
    # Verificar el resultado
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # El archivo debería permanecer sin cambios ya que no hay línea @Languages
    assert content == test_content
    
    # Limpieza
    os.remove(test_file) 