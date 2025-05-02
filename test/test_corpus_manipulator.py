import unittest
import os
import shutil
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.corpus_manipulator import CorpusManipulator

class TestCorpusManipulator(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.test_dir = "test_corpus"
        self.test_output_dir = "test_corpus_modified"
        
        # Crear directorios de prueba
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Crear un archivo de prueba
        self.test_file = os.path.join(self.test_dir, "test_child", "000828.cha")
        os.makedirs(os.path.dirname(self.test_file), exist_ok=True)
        
        # Contenido de prueba
        test_content = """@UTF8
@PID: eng|CHILDES|Post|Lew|000828|2;0|female|Target_Child|typical
@Languages: eng
@Participants: CHI Lew Target_Child, MOT Mother, FAT Father
@Options: utf8
@Media: video, audio
@Date: 2000-08-28
@Types: CHI Target_Child, MOT Mother, FAT Father
*CHI: hola mama.
%mor: hola mama
%gra: 1|1|INTJ 2|2|N
*MOT: hola cariño.
%mor: hola cariño
%gra: 1|1|INTJ 2|2|N
"""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Inicializar el manipulador
        self.manipulator = CorpusManipulator()
        self.manipulator.base_dir = self.test_dir
        self.manipulator.output_dir = self.test_output_dir
    
    def tearDown(self):
        """Limpieza después de las pruebas"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
    
    def test_calculate_age_from_filename(self):
        """Prueba el cálculo de edad a partir del nombre del archivo"""
        # Probar formato AAMMDD
        age = self.manipulator.extract_age(self.test_file)
        self.assertEqual(age, "2;0")
        
        # Probar formato x1-[r|f]DDmmmYY
        test_file2 = os.path.join(self.test_dir, "test_child", "x1-r15jan00.cha")
        test_content2 = """@UTF8
@PID: eng|CHILDES|Post|Lew|x1-r15jan00|1;6|female|Target_Child|typical
@Languages: eng
*CHI: hola mama."""
        with open(test_file2, 'w', encoding='utf-8') as f:
            f.write(test_content2)
        age = self.manipulator.extract_age(test_file2)
        self.assertEqual(age, "1;6")
    
    def test_insert_age_metadata(self):
        """Prueba la inserción de metadatos de edad y nombre"""
        input_path = self.test_file
        output_path = os.path.join(self.test_output_dir, "test_child", "000828.cha")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        age = self.manipulator.extract_age(input_path)
        self.manipulator.modify_file(input_path, output_path, age)
        
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        self.assertIn("@Age: 2;0", content)
        self.assertIn("@ChildName: Lew", content)
    
    def test_process_directory(self):
        """Prueba el procesamiento completo del directorio"""
        self.manipulator.process_directory()
        
        # Verificar que el archivo de salida existe y contiene los metadatos
        output_file = os.path.join(self.test_output_dir, "test_child", "000828.cha")
        self.assertTrue(os.path.exists(output_file))
        
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        self.assertIn("@Age: 2;0", content)
        self.assertIn("@ChildName: Lew", content)

if __name__ == '__main__':
    unittest.main() 