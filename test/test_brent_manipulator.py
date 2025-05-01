import unittest
import os
import shutil
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.brent_manipulator import BrentManipulator

class TestBrentManipulator(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear directorios de prueba
        self.test_dir = "test_brent"
        self.test_output_dir = "test_brent_modified"
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Crear un archivo de prueba
        self.test_file_content = """@UTF8
@PID:	11312/c-00015477-1
@Begin
@Languages:	eng
@Participants:	MOT Mother, CHI Target_Child
@Options:	multi
@ID:	eng|Brent|MOT||female|||Mother|||
@ID:	eng|Brent|CHI|0;08.28|male|||Target_Child|||
@Media:	000828, audio"""
        
        # Crear un directorio de prueba y archivo
        self.test_child_dir = os.path.join(self.test_dir, "c1")
        os.makedirs(self.test_child_dir, exist_ok=True)
        self.test_file_path = os.path.join(self.test_child_dir, "000828.cha")
        with open(self.test_file_path, 'w', encoding='utf-8') as f:
            f.write(self.test_file_content)
            
        # Inicializar el manipulador
        self.manipulator = BrentManipulator(self.test_dir, self.test_output_dir)
        
    def tearDown(self):
        """Limpieza después de las pruebas"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
            
    def test_calculate_age_from_filename(self):
        """Prueba el cálculo de edad a partir del nombre del archivo"""
        # Prueba con formato AAMMDD
        age = self.manipulator._calculate_age_from_filename("000828.cha")
        self.assertEqual(age["years"], 0)
        self.assertEqual(age["months"], 8)
        self.assertEqual(age["days"], 28)
        
        # Prueba con formato x1-[r|f]DDmmmYY
        age = self.manipulator._calculate_age_from_filename("m1-r15jun00.cha")
        self.assertEqual(age["years"], 0)
        self.assertEqual(age["months"], 6)
        self.assertEqual(age["days"], 15)
        
    def test_insert_age_metadata(self):
        """Prueba la inserción de metadatos de edad y nombre"""
        age = {"years": 0, "months": 8, "days": 28}
        child_name = "Morgan"
        
        modified_content = self.manipulator._insert_age_metadata(
            self.test_file_content, age, child_name
        )
        
        # Verificar que los metadatos se insertaron correctamente
        self.assertIn("@Child_Age: 00 years 08 months 28 days", modified_content)
        self.assertIn("@ChildName: Morgan", modified_content)
        
    def test_process_directory(self):
        """Prueba el procesamiento completo del directorio"""
        # Procesar el directorio
        self.manipulator.process_directory()
        
        # Verificar que se creó el archivo de salida
        output_file = os.path.join(self.test_output_dir, "Morgan", "000828.cha")
        self.assertTrue(os.path.exists(output_file))
        
        # Verificar el contenido del archivo de salida
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("@Child_Age: 00 years 08 months 28 days", content)
            self.assertIn("@ChildName: Morgan", content)

if __name__ == '__main__':
    unittest.main() 