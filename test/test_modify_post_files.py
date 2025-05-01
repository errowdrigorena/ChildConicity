import os
import pytest
import shutil
from src.modify_post_files import extract_age, modify_cha_file, process_directory

@pytest.fixture
def test_files():
    """Fixture para crear archivos de prueba temporales"""
    # Crear directorio temporal para las pruebas
    test_dir = "test_post_files"
    os.makedirs(test_dir, exist_ok=True)
    
    # Crear archivo con edad válida
    valid_age_content = """@UTF8
@PID: test
@Begin
@Languages: eng
@Participants: CHI Target_Child
@ID: eng|Post|CHI|1;06.26|male|TD||Target_Child|||
"""
    valid_file = os.path.join(test_dir, "valid_age.cha")
    with open(valid_file, 'w', encoding='utf-8') as f:
        f.write(valid_age_content)
    
    # Crear archivo sin edad
    no_age_content = """@UTF8
@PID: test
@Begin
@Languages: eng
@Participants: CHI Target_Child
@ID: eng|Post|CHI||male|TD||Target_Child|||
"""
    no_age_file = os.path.join(test_dir, "no_age.cha")
    with open(no_age_file, 'w', encoding='utf-8') as f:
        f.write(no_age_content)
    
    # Crear archivo sin línea @Languages
    no_lang_content = """@UTF8
@PID: test
@Begin
@Participants: CHI Target_Child
@ID: eng|Post|CHI|1;06.26|male|TD||Target_Child|||
"""
    no_lang_file = os.path.join(test_dir, "no_lang.cha")
    with open(no_lang_file, 'w', encoding='utf-8') as f:
        f.write(no_lang_content)
    
    yield {
        'valid_file': valid_file,
        'no_age_file': no_age_file,
        'no_lang_file': no_lang_file,
        'test_dir': test_dir
    }
    
    # Limpieza después de las pruebas
    shutil.rmtree(test_dir)

def test_extract_age(test_files):
    """Prueba la función extract_age"""
    # Caso 1: Edad válida
    expected_age = "1 years 06 months 26 days"
    assert extract_age(test_files['valid_file']) == expected_age
    
    # Caso 2: Archivo sin edad
    assert extract_age(test_files['no_age_file']) is None
    
    # Caso 3: Archivo que no existe
    assert extract_age("archivo_inexistente.cha") is None

def test_modify_cha_file(test_files):
    """Prueba la función modify_cha_file"""
    # Caso 1: Archivo con línea @Languages
    child_name = "TestChild"
    age = "1 years 06 months 26 days"
    modify_cha_file(test_files['valid_file'], child_name, age)
    
    with open(test_files['valid_file'], 'r', encoding='utf-8') as f:
        content = f.read()
    
    expected_content = """@UTF8
@PID: test
@Begin
@Languages: eng
@ChildName: TestChild
@Child_Age: 1 years 06 months 26 days
@Participants: CHI Target_Child
@ID: eng|Post|CHI|1;06.26|male|TD||Target_Child|||
"""
    assert content == expected_content
    
    # Caso 2: Archivo sin línea @Languages
    original_content = open(test_files['no_lang_file'], 'r', encoding='utf-8').read()
    modify_cha_file(test_files['no_lang_file'], child_name, age)
    modified_content = open(test_files['no_lang_file'], 'r', encoding='utf-8').read()
    assert original_content == modified_content

@pytest.fixture
def test_directory_structure(tmp_path):
    """Fixture para crear una estructura de directorios de prueba"""
    # Crear estructura de directorios temporal usando tmp_path
    test_root = tmp_path / "Post"
    test_root.mkdir()
    
    # Crear archivos de metadatos
    (test_root / "0metadata.cdc").write_text("Test metadata")
    (test_root / "0types.txt").write_text("Test types")
    
    # Crear subdirectorios y archivos .cha
    subdirs = ["Lew", "She", "Tow"]
    for subdir in subdirs:
        subdir_path = test_root / subdir
        subdir_path.mkdir()
        (subdir_path / "test.cha").write_text("""@UTF8
@PID: test
@Begin
@Languages: eng
@Participants: CHI Target_Child
@ID: eng|Post|CHI|1;06.26|male|TD||Target_Child|||
""")
    
    yield tmp_path
    
    # La limpieza es automática con tmp_path

def test_process_directory(test_directory_structure, monkeypatch):
    """Prueba la función process_directory"""
    # Modificar la función para usar el directorio de prueba
    original_dirname = os.path.dirname
    
    def mock_dirname(path):
        if path == __file__:
            return original_dirname(path)
        return str(test_directory_structure)
    
    monkeypatch.setattr(os.path, 'dirname', mock_dirname)
    
    # Ejecutar process_directory
    process_directory()
    
    # Verificar que se creó el directorio Post_modified
    modified_dir = os.path.join(str(test_directory_structure), "Post_modified")
    assert os.path.exists(modified_dir)
    
    # Verificar que se copiaron los archivos de metadatos
    assert os.path.exists(os.path.join(modified_dir, "0metadata.cdc"))
    assert os.path.exists(os.path.join(modified_dir, "0types.txt"))
    
    # Verificar que se crearon los subdirectorios
    for subdir in ["Lew", "She", "Tow"]:
        subdir_path = os.path.join(modified_dir, subdir)
        assert os.path.exists(subdir_path)
        test_file = os.path.join(subdir_path, "test.cha")
        assert os.path.exists(test_file)
        
        # Verificar que se añadieron los metadatos
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert f"@ChildName: {subdir}" in content
            assert "@Child_Age: 1 years 06 months 26 days" in content
    
    # Limpieza
    shutil.rmtree(modified_dir) 