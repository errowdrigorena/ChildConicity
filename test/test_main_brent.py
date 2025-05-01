import os
import pytest
from unittest.mock import patch, MagicMock
from src.main_brent import main

class TestMainBrent:
    @patch('src.main_brent.BrentManipulator')
    def test_successful_processing(self, mock_manipulator):
        """Test cuando el procesamiento es exitoso"""
        # Configurar el mock
        mock_instance = MagicMock()
        mock_manipulator.return_value = mock_instance
        
        # Ejecutar main
        with patch('builtins.print') as mock_print:
            main()
            
        # Verificar que se creó la instancia y se llamó process_directory
        mock_manipulator.assert_called_once()
        mock_instance.process_directory.assert_called_once()
        mock_print.assert_called_with("Procesamiento completado exitosamente")
        
    @patch('src.main_brent.BrentManipulator')
    def test_directory_not_found(self, mock_manipulator):
        """Test cuando el directorio no existe"""
        # Configurar el mock para lanzar FileNotFoundError
        mock_instance = MagicMock()
        mock_instance.process_directory.side_effect = FileNotFoundError("El directorio no existe")
        mock_manipulator.return_value = mock_instance
        
        # Ejecutar main
        with patch('builtins.print') as mock_print:
            main()
            
        # Verificar el mensaje de error
        mock_print.assert_called_with("Error durante el procesamiento: El directorio no existe")
        
    @patch('src.main_brent.BrentManipulator')
    def test_permission_error(self, mock_manipulator):
        """Test cuando hay problemas de permisos"""
        # Configurar el mock para lanzar PermissionError
        mock_instance = MagicMock()
        mock_instance.process_directory.side_effect = PermissionError("Permiso denegado")
        mock_manipulator.return_value = mock_instance
        
        # Ejecutar main
        with patch('builtins.print') as mock_print:
            main()
            
        # Verificar el mensaje de error
        mock_print.assert_called_with("Error durante el procesamiento: Permiso denegado")
        
    @patch('src.main_brent.BrentManipulator')
    def test_file_processing_error(self, mock_manipulator):
        """Test cuando hay problemas al procesar archivos"""
        # Configurar el mock para lanzar un error genérico
        mock_instance = MagicMock()
        mock_instance.process_directory.side_effect = Exception("Error al procesar archivo")
        mock_manipulator.return_value = mock_instance
        
        # Ejecutar main
        with patch('builtins.print') as mock_print:
            main()
            
        # Verificar el mensaje de error
        mock_print.assert_called_with("Error durante el procesamiento: Error al procesar archivo")
        
    @patch('src.main_brent.BrentManipulator')
    def test_integration_with_real_files(self, mock_manipulator):
        """Test de integración con archivos reales"""
        # Crear directorio temporal y archivo de prueba
        test_dir = "test_brent"
        test_file = os.path.join(test_dir, "test.cha")
        
        try:
            os.makedirs(test_dir, exist_ok=True)
            with open(test_file, 'w') as f:
                f.write("@Languages: eng\n")
            
            # Configurar el mock para usar el directorio de prueba
            mock_instance = MagicMock()
            mock_manipulator.return_value = mock_instance
            
            # Ejecutar main
            with patch('builtins.print') as mock_print:
                main()
                
            # Verificar que se llamó process_directory
            mock_instance.process_directory.assert_called_once()
            mock_print.assert_called_with("Procesamiento completado exitosamente")
            
        finally:
            # Limpiar archivos de prueba
            if os.path.exists(test_file):
                os.remove(test_file)
            if os.path.exists(test_dir):
                os.rmdir(test_dir) 